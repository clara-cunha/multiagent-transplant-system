import jsonpickle
from spade.behaviour import CyclicBehaviour

class ARListen(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=30)
        if msg:
            performative = msg.get_metadata("performative")

            if performative == "inform":
                patient = jsonpickle.decode(msg.body)
                self.agent.patient_dic[patient.getOrgan().getName()].append(patient)

            else:
                print(f"Message not recognized: MyJID:{self.agent.jid}; SenderJID:{msg.sender}, performative:{performative}")
        else:
            print(f"Agent {str(self.agent.jid)} did not received any message after 30 seconds")