"""
Project for:
    BBT.HTI.508 Health Software Development Project
    Spring 2022

Made by:
    Olivia Aarikka:)
    Anni Hakola
    Miina Rautakorpi:)
    Tuulia Laakso

Instructions:
    This application analyses blood sample data and presents the analysis to a healthcare professional.
"""

import json
import re
import tkinter
from tkinter import *
import requests
from pprint import pprint


class Patient:
    def __init__(self, id, name, bE, bK, gB, gS):
        self.__id = id
        self.__name = name

        #Näihin listoihin tallennetaan yksittäisiä veriarvoja aikajärjestyksessä. Ei vielä käytössä missään.
        #Muukin muoto kuin lista voisi toimia.
        #self.__glucoseB = {ajankohda: [arvo: viitearvoissa]}
        self.__bilirubE = bE
        self.__bilirubK = bK
        self.__glucoseB = gB
        self.__glucoseS = gS

        # En oo varma toimiiko nää listat näin?
        '''self.__bilirubE.append(bE)
        self.__bilirubK.append(bK)
        self.__glucoseB.append(gB)
        self.__glucoseS.append(gS)'''

    def return_id_name(self):
        return int(self.__id), str(self.__name)

    def return_name(self):
        return str(self.__name)

    def return_bilirubinE(self):
        return self.__bilirubE

    def return_bilirubinK(self):
        return self.__bilirubK


    def return_blood_values(self):
        return self.__glucoseB, self.__glucoseS, self.__bilirubE, self.__bilirubK

    def print_self(self):
        pprint("Printing information of patient:")
        pprint(self.__id)
        pprint(self.__name)


class SimpleFHIRClient(object):
    def __init__(self, server_url, server_user, server_password, debug=False):
        self.debug = debug
        self.server_url = server_url
        self.server_user = server_user
        self.server_password = server_password

    def get_all_patients(self):
        requesturl = self.server_url + "/Patient?_format=json"
        entries = self._get_json(requesturl)["entry"]
        return [entry["resource"] for entry in entries]

    def get_all_data_for_patient(self, patient_id):
        requesturl = self.server_url + "/Patient/" + \
            patient_id + "$everything?_format=json"
        return self._get_json(requesturl)["entry"]

    def _get_json(self, requesturl):
        response = requests.get(requesturl,
                                auth=(self.server_user, self.server_password))
        response.raise_for_status()
        result = response.json()
        if self.debug:
            pprint(result)
        return result



class HealthSofta:
    def __init__(self):
        self.__main_window = Tk()
        self.__main_window.title("HealthSofta")
        self.__main_window.geometry("800x800")
        self.__main_window.configure(bg='white', borderwidth=10)
        self.__main_window.rowconfigure(0, {'minsize': 2})


        #Tässä dictissä on keynä potilaan id, ja sen jälkeen potilasolento.

        self.__PATIENTS = {}

        #Creating components for UI
        self.__headerLabel = Label(self.__main_window, text="Welcome to HealthSofta!", font=("Helvetica", 18),
                                   bg='#33FFB0')
        self.__headerLabel.grid(row=0, column=0, sticky=NW, columnspan=2)
        #self.__welcomeLabel.place(x=90, y=0)
        #self.__main_window.label

        self.__explText = Label(self.__main_window, font=("Helvetica", 12), highlightthickness=0,
                                highlightcolor='white', text="Press Start to download latest results from your\n"
                                                             "patients' devices. After that you can see the\nanalysed "
                                                             "data.", bg='white')

        self.__explText.grid(row=1, column=0, sticky=NW, columnspan=2)
        #self.__explText.pack()

        #self.__explText = Text(self.__main_window, font=("Helvetica", 12), width=40, height=10, highlightthickness=0, borderwidth=0)
        #self.__explText.insert(INSERT, "Press Start to download latest results from your\n patients' devices. "
        #                                    "After that you\ncan see the analysed data.")
        #self.__explText.grid(row=3, column=0, rowspan=2)
        #self.__explText.place(x=0, y=30)
        #self.__Text2 = Text(self.__main_window, font=("Helvetica", 12))
        #self.__Text2.grid(row=5, column=0)

        self.__textValues = Label(text=" ", font=("Helvetica", 12), bg='white')
        self.__textValues.grid(row=5, column=1)
        self.__textValues2 = Label(fg='red', bg='white')
        self.__textValues2.grid(row=5, column=2)

        self.__buttonLogo = Button(self.__main_window, text="LOGO HERE", font=(16), state="disabled", height=4)
        self.__buttonLogo.grid(row=0, column=6, rowspan=3)

        #self.__startButton = Button(self.__main_window, text="Start", command=self.create_patients())
        self.__startButton = Button(self.__main_window, text="Start", command=self.create_patients, bg='#75FF30')
        self.__exitButton = Button(self.__main_window, text="Exit", command=self.exit)

        #Creating grid-layout for components

        self.__startButton.grid(row=6, column=0, sticky=SW)
        self.__startButton.configure(width=5)
        self.__exitButton.grid(row=6, column=2, sticky=SW)
        self.__exitButton.configure(width=5)




    #Tähän kohtaan HealthSofta -classin alle tulee suurin osa funktioista.

    def back(self):
        self.__main_window.destroy()
        self.__init__()


    def create_patients(self):
        client = SimpleFHIRClient(
            server_url="http://tutsgnfhir.com",
            server_user="tutfhir",
            server_password="tutfhir1")
        all_patients = client.get_all_patients()

        i = 0

        # Testailua näiden avulla
        '''all_data_patient = client.get_all_data_for_patient(all_patients[0]["id"])
        print(all_patients[49]['id'])
        print(all_data_patient[49]['resource']['text']['div'][0])
        print(all_data_patient[49]['resource']['code']['coding'][0]['display'])'''


        for patient_record in all_patients:

            bilirub_K_list = []
            bilirub_E_list = []
            glucose_B_list = []
            glucose_S_list = []

            '''bilirub_K_list.clear()
            bilirub_E_list.clear()
            glucose_B_list.clear()
            glucose_S_list.clear()'''


            # Käy läpi potilaat ja tallentaa oikeet arvot listoihin
            # <div>2006-12-23: Glucose SerPl-mCnc = 96 mg/dL</div> tässä muodossa listassa
            
            # potilas
            all_data_patient = client.get_all_data_for_patient(all_patients[i]["id"])

            # potilaan tiedot
            for tmp in all_data_patient:
                if tmp['resource']['resourceType'] == 'Observation':
                    if tmp['resource']['code']['coding'][0]['display'] == "Bilirub Skin-mCnc":
                        bilirub_K = tmp['resource']['text']['div']
                        bilirub_K_list.append(bilirub_K)
                        print(bilirub_K)

                    if tmp['resource']['code']['coding'][0]['display'] == "Bilirub SerPl-mCnc":
                        bilirub_E = tmp['resource']['text']['div']
                        bilirub_E_list.append(bilirub_E)
                        print (bilirub_E)

                    if tmp['resource']['code']['coding'][0]['display'] == "Glucose Bld-mCnc":
                        glucose_B = tmp['resource']['text']['div']
                        glucose_B_list.append(glucose_B)
                        print(glucose_B)

                    if tmp['resource']['code']['coding'][0]['display'] == "Glucose SerPl-mCnc":
                        glucose_S = tmp['resource']['text']['div']
                        glucose_S_list.append(glucose_S)
                        print(glucose_S)

            # Bilirub E:
            #http://tutsgnfhir.com/Observation/Observation-879-lab patient 665677

            # Glucose B:
            #http://tutsgnfhir.com/Observation/Observation-897-lab patient 665677
            #http://tutsgnfhir.com/Observation/Observation-898-lab patient 665677

            # Glucose S:
            #http://tutsgnfhir.com/Observation/Observation-878-lab 665677
            #http://tutsgnfhir.com/Observation/Observation-904-lab 665677
            #http://tutsgnfhir.com/Observation/Observation-919-lab 665677
            #http://tutsgnfhir.com/Observation/Observation-932-lab 665677
            #http://tutsgnfhir.com/Observation/Observation-954-lab 665677
            #http://tutsgnfhir.com/Observation/Observation-976-lab 665677

            patient_id = patient_record["id"]
            print(patient_id)
            patient_given = patient_record["name"][0]["given"][0]
            new_patient = Patient(patient_id, patient_given, bilirub_K_list, bilirub_E_list, glucose_B_list, glucose_S_list)
            self.__PATIENTS[patient_id] = new_patient

            i += 1

        self.__headerLabel['text'] = "Search for a patient to continue"

        self.__explText['text'] = "Instructions here."
        self.__Text2 = Label(self.__main_window, text="Give the ID of the patient:", font=("Helvetica", 12), bg='white')
        self.__Text2.grid(row=4, column=0, sticky=NW)
        # self.__explText.delete(1.0, "end")
        # self.__explText.insert(1.0, "Instructions here.\n\n\nGive the ID of the patient: ")
        # self.__Text2.insert(1.0, "Give the ID of the patient: ")

        self.__entryID = Entry(self.__main_window, borderwidth=2)
        self.__entryID.grid(row=4, column=1, sticky=NW)
        self.__ID = self.__entryID.get()
        self.__entryButton = Button(self.__main_window, text="Search", command=self.search)
        # entryButtoniin tulee commandiksi oikeasti potilaan hakeminen ID:n avulla
        self.__entryButton.grid(row=4, column=2, sticky=NW)
        self.__entryButton.configure(height=1, width=6)

        self.__emptyText = Label(self.__main_window, bg='white', text=" ")
        self.__emptyText.grid(row=5, column=0, sticky=NW)

        self.__startButton['text'] = "Back"
        self.__startButton['command'] = self.back
        self.__startButton['bg'] = "#f0f0f0"



    def search(self):
        self.__ID = self.__entryID.get()
        if not self.__ID:
            self.__emptyText['text'] = "You did not give any ID. Please, write an ID\nand then press Searh"

        else:

            #Check if the ID exists in the dict
            if self.__ID in self.__PATIENTS:
                self.__entryID.destroy()
                self.__patient = self.__PATIENTS[self.__ID]
                self.__name = self.__patient.return_name()
                self.__headerLabel['text'] = self.__name
                self.__emptyText['text'] = " "
                self.__Text2['text'] = "The given ID is:"
                self.__startButton['command'] = self.back_to_search
                self.__explText['text'] = self.__ID

                self.__textValues['text'] = "BilirubinK values are:"
                #self.__textValues.grid(row=5,column=1)
                #self.__textValues2 = Label(fg='red')
                self.__textValues2['text'] = self.__patient.return_bilirubinK()
                #self.__textValues2.grid(row=5, column=2)

                self.__entryButton.destroy()


            else:
                self.__emptyText['text'] = "The given  ID was not found in the database.\nTry to give another one, please."
                #self.__emptyText['font-color'] = 'red'






    def back_to_search(self):
        self.__headerLabel['text'] = "Search for a patient to continue"

        self.__explText['text'] = "Instructions here."
        self.__Text2 = Label(self.__main_window, text="Give the ID of the patient:", font=("Helvetica", 12), bg='white')
        self.__Text2.grid(row=4, column=0, sticky=NW)
        # self.__explText.delete(1.0, "end")
        # self.__explText.insert(1.0, "Instructions here.\n\n\nGive the ID of the patient: ")
        # self.__Text2.insert(1.0, "Give the ID of the patient: ")

        self.__entryID = Entry(self.__main_window, borderwidth=2)
        self.__entryID.grid(row=4, column=1, sticky=NW)
        self.__ID = self.__entryID.get()
        self.__entryButton = Button(self.__main_window, text="Search", command=self.search)
        # entryButtoniin tulee commandiksi oikeasti potilaan hakeminen ID:n avulla
        self.__entryButton.grid(row=4, column=2, sticky=NW)
        self.__entryButton.configure(height=1, width=6)

        self.__textValues['text'] = " "
        self.__textValues2['text'] = " "

        self.__startButton['text'] = "Back"
        self.__startButton['command'] = self.back
        self.__startButton['bg'] = "#f0f0f0"



    def exit(self):
        self.__main_window.destroy()


    def start(self):
        self.__main_window.mainloop()


def main():
    user_interference = HealthSofta()
    user_interference.start()

main()
