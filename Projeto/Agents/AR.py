from spade import agent

from Projeto.Classes.organ import organ_type_dic
from Projeto.Behaviours.AR.AR_listen import ARListen
from Projeto.Behaviours.AR.AR_send import ARSend

class AR(agent.Agent):

    patient_dic = {} #{"organ_type": [patient1, patient2, ...]}

    for organ in organ_type_dic.keys():
        if organ not in patient_dic.keys():
            patient_dic[organ] = []

    async def setup(self):
        print('\nAR starting...\n')

        a = ARListen()
        b = ARSend(period=5)
        self.add_behaviour(a)
        self.add_behaviour(b)