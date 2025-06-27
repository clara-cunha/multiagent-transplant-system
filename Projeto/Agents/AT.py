from spade import agent

from Projeto.Behaviours.AT.AT_listen import ATListen
from Projeto.Behaviours.AT.AT_send import ATSend
from Projeto.Behaviours.AT.pass_time import PassTime
from Projeto.Classes.organ import organ_type_dic

class AT(agent.Agent):

    async def setup(self):
        print("\nAT starting...\n")

        self.torgan_tuple_list = [] #[(torgan1, hospital1), (torgan2, hospital2), ...]
        self.current_requests = [] #[message1, message2, ...]
        self.patient_dic = {} #{"organ_type": [patient1, patient2, ...]}
        self.hospital_list = [] #[hospital1, hospital2, ...]

        for organ_type in organ_type_dic.keys():
            self.patient_dic[organ_type] = []

        a = ATListen()
        b = ATSend()
        c = PassTime(period = 1)
        self.add_behaviour(a)
        self.add_behaviour(b)
        self.add_behaviour(c)