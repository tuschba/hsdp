"""
Project for:
 BBT.HTI.508 Health Software Development Project

Made by:
Olivia Aarikka
Anni Hakola
Miina Rautakorpi
Tuulia Laakso

Instructions:
This application analyses blood data.
"""

import json
from tkinter import *
import requests
from pprint import pprint


class Patient:
    def __init__(self, id, name):
        self.__id = id
        self.__name = name

        # Näihin listoihin tallennetaan yksittäisiä veriarvoja int-muodossa aikajärjestyksessä.
        self.__glucoseB = []
        self.__glucoseS = []
        self.__bilirubE = []
        self.__bilirubK = []

    def return_id(self):
        return int(self.__id)

    def return_blood_values(self):
        return self.__glucoseB, self.__glucoseS, self.__bilirubE, self.__bilirubK

    def print_self(self):
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

        self.__PATIENTS = []
        self.__PATIENT_NAMES = []


    #Tähän HealthSofta -classin alle tulee suurin osa funktioista.


    def create_patients(self):
        client = SimpleFHIRClient(
            server_url="http://tutsgnfhir.com",
            server_user="tutfhir",
            server_password="tutfhir1")
        all_patients = client.get_all_patients()

        # List all found patients
        for patient_record in all_patients:
            patient_id = patient_record["id"]
            patient_given = patient_record["name"][0]["given"][0]
            new_patient = Patient(patient_id, patient_given)
            self.__PATIENTS.append(new_patient)
            self.__PATIENT_NAMES.append(patient_given)

        for i in self.__PATIENT_NAMES:
            pprint(i)



    def start(self):
        self.__main_window.mainloop()


def main():
    user_interference = HealthSofta()
    user_interference.start()
    user_interference.create_patients()


main()
