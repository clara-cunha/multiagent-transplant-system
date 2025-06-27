class KillChart:
    def __init__(self, organ, patient, hospital):
        self.organ = organ
        self.patient = patient
        self.hospital = hospital
        self.kill_organ = False
        self.kill_patient = False

    def getOrgan(self):
        return self.organ

    def getPatient(self):
        return self.patient

    def getHospital(self):
        return self.hospital

    def getKillOrgan(self):
        return self.kill_organ

    def getKillPatient(self):
        return self.kill_patient

    def setOrgan(self, organ):
        self.organ = organ

    def setPatient(self, patient):
        self.patient = patient

    def setHospital(self, hospital):
        self.hospital = hospital

    def setKillOrgan(self, kill_organ):
        self.kill_organ = kill_organ

    def setKillPatient(self, kill_patient):
        self.kill_patient = kill_patient