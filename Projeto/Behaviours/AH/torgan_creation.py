import jsonpickle
from spade.behaviour import CyclicBehaviour, PeriodicBehaviour
from spade.message import Message

from Projeto.parameters import XMPP_SERVER
from Projeto.Classes.organ import Organ

class TorganCreation(PeriodicBehaviour):
    async def run(self):
        h_jid = str(self.agent.hospital.get_jid())
        id_hospital = h_jid[2:h_jid.index('@')]

        torgan = Organ('H' + id_hospital + '-O' + str(self.agent.id_atual_organ))
        self.agent.id_atual_organ += 1

        msg = Message(to = "AT@" + XMPP_SERVER)
        msg.body = jsonpickle.encode( (torgan, self.agent.hospital) )
        msg.set_metadata("performative", "subscribe_torgan")

        await self.send(msg)