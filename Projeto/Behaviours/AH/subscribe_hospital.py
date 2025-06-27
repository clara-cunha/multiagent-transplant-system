import jsonpickle
from spade.behaviour import OneShotBehaviour
from spade.message import Message

from Projeto.parameters import XMPP_SERVER

class SubscribeHospital(OneShotBehaviour):
    async def run(self):

        msg = Message(to = 'AT@' + XMPP_SERVER)
        msg.body = jsonpickle.encode(self.agent.hospital)
        msg.set_metadata('performative', 'subscribe')

        await self.send(msg)
