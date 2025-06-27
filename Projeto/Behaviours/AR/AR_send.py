import jsonpickle
from spade.behaviour import PeriodicBehaviour
from spade.message import Message

from Projeto.parameters import XMPP_SERVER

class ARSend(PeriodicBehaviour):
    async def run(self):
        print("\nSending new patients\n")

        msg = Message(to = 'AT@' + XMPP_SERVER)
        msg.body = jsonpickle.encode(self.agent.patient_dic)
        msg.set_metadata("performative", "inform_patient_list")

        for key in self.agent.patient_dic.keys():
            self.agent.patient_dic[key] = []

        await self.send(msg)