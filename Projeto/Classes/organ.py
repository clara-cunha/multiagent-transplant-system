import random
from Projeto.parameters import organ_type_dic, ABO, RH

class Organ:
    def __init__(self, id):
        self.id = id
        self.name = random.choice(list(organ_type_dic.keys()))
        self.ABO = random.choice(ABO)
        self.Rh = random.choice(RH)
        self.ischemia_time = organ_type_dic[self.name]['ischemia_time']
        self.op_time = organ_type_dic[self.name]['op_time']
        self.op_kill_organ = organ_type_dic[self.name]['op_kill_organ']
        self.op_kill_patient = organ_type_dic[self.name]['op_kill_patient']
        self.hold = False


    def getName(self):
        return self.name

    def getABO(self):
        return self.ABO

    def getRh(self):
        return self.Rh

    def getIschemiaTime(self):
        return self.ischemia_time

    def getOpTime(self):
        return self.op_time

    def getHOLD(self):
        return self.hold

    def getID(self):
        return self.id

    def getOpKillOrgan(self):
        return self.op_kill_organ

    def getOpKillPatient(self):
        return self.op_kill_patient

    def setOpKillOrgan(self, kill_organ):
        self.op_kill_organ = kill_organ

    def setOpKillPatient(self, kill_patient):
        self.op_kill_patient = kill_patient

    def setID(self, id: str):
        self.id = id

    def setHOLD(self, hold: bool):
        self.hold = hold

    def setName(self, name: str):
        self.name = name

    def setABO(self, ABO: str):
        self.ABO = ABO

    def setRh(self, Rh: str):
        self.Rh = Rh

    def setIschemiaTime(self, ischemia_time: int):
        self.ischemia_time = ischemia_time

    def setOpTime(self, op_time: int):
        self.op_time = op_time

    def __str__(self):
        return f"Organ {self.id}: {self.name}; type: {self.ABO + self.Rh}"