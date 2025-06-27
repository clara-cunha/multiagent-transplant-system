import random
from Projeto.Classes.hospital import Hospital
from Projeto.Classes.organ import Organ
from Projeto.parameters import min_start_urg, max_start_urg

class Patient:
    def __init__(self, id, organ:Organ, hospital:Hospital):
        self.id = id
        self.organ = organ
        self.hospital = hospital
        self.urgency = random.randint(min_start_urg, max_start_urg)
        self.no_room = False

    def getID(self):
        return self.id

    def getOrgan(self):
        return self.organ

    def getHospital(self):
        return self.hospital

    def getUrgency(self):
        return self.urgency

    def getNoRoom(self):
        return self.no_room

    def setNoRoom(self, value):
        self.no_room = value

    def setID(self, id:str):
        self.id = id

    def setOrgan(self, organ:Organ):
        self.organ = organ

    def setHospital(self, hospital:Hospital):
        self.hospital = hospital

    def setUrgency(self, urgency:int):
        self.urgency = urgency

    def __str__(self):
        return f"Patient {self.id}: organ: {self.organ.name}; type: {self.organ.ABO + self.organ.Rh}; urgency: {self.urgency}"