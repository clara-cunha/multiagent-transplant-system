import jsonpickle
from spade.behaviour import PeriodicBehaviour
from spade.message import Message

from Projeto.parameters import XMPP_SERVER
from Projeto.Classes.organ import Organ
from Projeto.Classes.patient import Patient

class PatientCreation(PeriodicBehaviour):

    async def run(self):

        h_jid = str(self.agent.hospital.get_jid())
        id_hospital = h_jid[2:h_jid.index('@')]

        patient = Patient('H' + id_hospital + '-P' + str(self.agent.id_atual_pat), Organ('pat_organ'), self.agent.hospital)
        self.agent.id_atual_pat += 1

        msg = Message(to = 'AR@' + XMPP_SERVER)
        msg.body = jsonpickle.encode(patient)
        msg.set_metadata('performative', 'inform')

        await self.send(msg)