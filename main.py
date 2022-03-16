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
from tkinter import *
import requests
from pprint import pprint


class Patient:
    def __init__(self, id, name):
        self.__id = id
        self.__name = name

        #Näihin listoihin tallennetaan yksittäisiä veriarvoja aikajärjestyksessä. Ei vielä käytössä missään.
        #Muukin muoto kuin lista voisi toimia.
        #self.__glucoseB = {ajankohda: [arvo: viitearvoissa]}
        self.__glucoseS = []
        self.__bilirubE = []
        self.__bilirubK = []

    def return_id_name(self):
        return int(self.__id), str(self.__name)

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

        #Tässä dictissä on keynä potilaan id, ja sen jälkeen potilasolento.
        self.__PATIENTS = {}

        #Creating components for UI
        self.__startButton = Button(self.__main_window, text="Start", command=self.create_patients())
        self.__exitButton = Button(self.__main_window, text="Exit", command=self.exit)

        #Creating grid-layout for components
        self.__startButton.grid(row=0, column=0, sticky=W)
        self.__exitButton.grid(row=1, column=0, sticky=W)


    #Tähän kohtaan HealthSofta -classin alle tulee suurin osa funktioista.


    def create_patients(self):
        client = SimpleFHIRClient(
            server_url="http://tutsgnfhir.com",
            server_user="tutfhir",
            server_password="tutfhir1")
        all_patients = client.get_all_patients()

        for patient_record in all_patients:


            #Tässä kohtaa luetaan veriarvot oliolle

            patient_id = patient_record["id"]
            patient_given = patient_record["name"][0]["given"][0]
            new_patient = Patient(patient_id, patient_given)
            self.__PATIENTS[patient_id] = new_patient




    def exit(self):
        self.__main_window.destroy()


    def start(self):
        self.__main_window.mainloop()


def main():
    user_interference = HealthSofta()
    user_interference.start()


main()
