from random import randint
from spade import agent

from Projeto.Behaviours.AH.AH_listen import AHListen
from Projeto.Behaviours.AH.torgan_creation import TorganCreation
from Projeto.Classes.hospital import Hospital
from Projeto.Behaviours.AH.patient_creation import PatientCreation
from Projeto.Behaviours.AH.subscribe_hospital import SubscribeHospital
from Projeto.parameters import min_rooms, max_rooms, min_teams, max_teams, min_pat_period, max_pat_period, \
    min_org_period, max_org_period

class AH(agent.Agent):

    async def setup(self):
        self.hospital = Hospital(str(self.jid))

        self.available_rooms = randint(min_rooms, max_rooms)
        self.available_teams = randint(min_teams, max_teams)

        self.id_atual_pat = 1
        self.id_atual_organ = 1

        patient_creation_period = randint(min_pat_period, max_pat_period)
        organ_creation_period = randint(min_org_period, max_org_period)

        print(f"""\nAgent Hospital {self.jid} starting...
Location: {self.hospital.get_location()}; Heliport: {self.hospital.get_heliport()}
Available rooms: {self.available_rooms}; Available teams: {self.available_teams}
Patient Creation Period: {patient_creation_period}; Organ Creation Period: {organ_creation_period}\n""")

        a = PatientCreation(period=patient_creation_period)
        b = TorganCreation(period=organ_creation_period)
        c = AHListen()
        d = SubscribeHospital()
        self.add_behaviour(a)
        self.add_behaviour(b)
        self.add_behaviour(c)
        self.add_behaviour(d)