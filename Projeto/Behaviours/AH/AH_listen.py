import jsonpickle
from spade.behaviour import CyclicBehaviour
from spade.message import Message
from random import randint
from time import sleep

from Projeto.Classes.kill_chart import KillChart
from Projeto.parameters import XMPP_SERVER

class AHListen(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout = 30)

        if msg:
            performative = msg.get_metadata('performative')

            if performative == "request_room":
                #quando recebe orgao atualiza rooms e teams, quando simula op repoe

                if self.agent.available_rooms > 0 and self.agent.available_teams > 0:
                    self.agent.available_rooms -= 1
                    self.agent.available_teams -= 1

                    torgan, hospital, patient = jsonpickle.decode(msg.body)

                    response = msg.make_reply()
                    response.body = msg.body
                    response.set_metadata('performative', 'confirm_room')
                    print(f"\n{self.agent.hospital}:\nConfirming conditions for {patient}.\nAvailable rooms: {self.agent.available_rooms}; Available teams: {self.agent.available_teams}.\n")
                    await self.send(response)

                else:
                    response = msg.make_reply()
                    response.body = msg.body
                    response.set_metadata('performative', 'refuse_room')

                    await self.send(response)

            elif performative == "confirm_transport":

                torgan, hospital, patient = jsonpickle.decode(msg.body)

                #simula op
                sleep(torgan.getOpTime())
                self.agent.available_rooms += 1
                self.agent.available_teams += 1
                print(f"\n{patient.getHospital()} finished procedure.\n{self.agent.available_rooms} rooms and {self.agent.available_teams} teams now available.\n")

                kill_chart = KillChart(torgan, patient, self.agent.hospital)

                if randint(1, 100) <= torgan.getOpKillPatient():
                    kill_chart.setKillPatient(True)
                    print(f"\nRIP {patient}!\n")

                if randint(1, 100) <= torgan.getOpKillOrgan():
                    kill_chart.setKillOrgan(True)
                    print(f"\nRIP {torgan}!!\n")


                if not kill_chart.getKillOrgan() and not kill_chart.getKillPatient():

                    print(f"\n{patient} was successfully implanted with {torgan}.\n")

                    final_msg_AT = Message(to = "AT@" + XMPP_SERVER)
                    final_msg_AT.body = msg.body
                    final_msg_AT.set_metadata('performative', 'confirm_op')
                    await self.send(final_msg_AT)

                else:
                    final_msg_AT = Message(to="AT@" + XMPP_SERVER)
                    final_msg_AT.body = jsonpickle.encode(kill_chart)
                    final_msg_AT.set_metadata('performative', 'failure_op')
                    await self.send(final_msg_AT)


            elif performative == "request_another_room":
                if self.agent.available_rooms > 0 and self.agent.available_teams > 0:
                    self.agent.available_rooms -= 1
                    self.agent.available_teams -= 1

                    torgan, _, patient, _ = jsonpickle.decode(msg.body)

                    hospital = self.agent.hospital

                    response = msg.make_reply()
                    response.body = msg.body
                    response.set_metadata('performative', 'confirm_another_room')
                    print(f"\n{hospital} confirmed conditions for {patient} from other hospital\n{self.agent.available_rooms} rooms and {self.agent.available_teams} teams now available.\n")
                    await self.send(response)

                else:
                    response = msg.make_reply()
                    response.body = msg.body
                    response.set_metadata('performative', 'refuse_another_room')

                    await self.send(response)

            else:
                print(f"Message not recognized: MyJID:{self.agent.jid}; SenderJID:{msg.sender}, performative:{performative}")

        else:
            print(f"Agent {str(self.agent.jid)} did not received any message after 30 seconds")