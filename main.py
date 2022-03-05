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

from tkinter import *

class Patient:
    def __init__(self, id):
        self.__id = id

        # Näihin listoihin tallennetaan yksittäisiä veriarvoja aikajärjestyksessä
        self.__glucoseB = []
        self.__glucoseS = []
        self.__bilirubE = []
        self.__bilirubK = []

    def return_id(self):
        return int(self.__id)

    def return_blood_values(self):
        return self.__glucoseB, self.__glucoseS, self.__bilirubE, self.__bilirubK


"""
class HealthSofta:
  def __init__(self):
      
      self.__main_window = Tk()
      self.__main_window.title("HealthSofta")
      """
#Tähän HealthSofta -classin alle tulee suurin osa funktioista, kun saadaan UI toimimaan. Siihen asti voi käyttää mainia.

def main():
    """
    user_interference = HealthSofta()
    user_interference.start()
    """


main()