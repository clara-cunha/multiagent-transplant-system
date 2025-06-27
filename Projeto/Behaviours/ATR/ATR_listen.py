from random import randint, uniform
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import jsonpickle
from time import sleep

from Projeto.functions import calc_time
from Projeto.parameters import failure_rate, XMPP_SERVER, delay_rate, urg_heli, max_start_urg

class ATRListen(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=30)
        if msg:
            performative = msg.get_metadata("performative")
            send = False

            if performative == "request_transport":
                request = jsonpickle.decode(msg.body)
                torgan, torgan_hospital, patient = request

                patient_hospital = patient.getHospital()

                urgent = patient.getUrgency() < max_start_urg * urg_heli

                travel_time = calc_time(patient_hospital, torgan_hospital, urgent)

                if travel_time == 0:
                    hospital_jid = str(patient_hospital.get_jid())
                    send = True
                    print(f"\n{torgan} was already at {patient_hospital} for {patient}\n")

                else:

                    #imaginando que corre mal

                    failure = (randint(1, 100) < failure_rate)
                    if failure:
                        failure_time = travel_time / randint(1, 10)
                        sleep(failure_time)

                        print(f"\n{torgan} failed to arrive at {patient_hospital}\n")

                        transport_message = Message(to="AT@" + XMPP_SERVER)
                        transport_message.body = jsonpickle.encode((torgan, torgan_hospital, patient))
                        transport_message.set_metadata("performative", "failure_transport")

                        await self.send(transport_message)

                    # imaginando que corre bem
                    else:
                        delay_bool = randint(1, 100) < delay_rate
                        delay_time = round(travel_time * uniform(0.1, 0.5), 2)

                        travel_time += delay_time * delay_bool

                        travel_time = round(travel_time, 2)

                        sleep(travel_time)

                        vehicle = "car"

                        if patient_hospital.get_heliport() and torgan_hospital.get_heliport() and patient.getUrgency() < max_start_urg * urg_heli:
                            vehicle = "helicopter"

                        print(f"\n{torgan} successfully arrived at {patient_hospital} for {patient} by {vehicle} in {travel_time} hours, including a delay of {delay_time * delay_bool} hours.\n")

                        hospital_jid = str(patient_hospital.get_jid())
                        send = True


            elif performative == "request_patient_transport":
                torgan, torgan_hospital, patient, result_list = jsonpickle.decode(msg.body)
                patient_hospital = patient.getHospital()
                destination_hospital = result_list[0]

                urgent = patient.getUrgency() < max_start_urg * urg_heli

                patient_travel_time = calc_time(patient_hospital, destination_hospital, urgent)
                organ_travel_time = calc_time(torgan_hospital, destination_hospital, urgent)

                time = max(organ_travel_time, patient_travel_time)

                # check max time

                delay_bool = randint(1, 100) < delay_rate
                delay_time = round(time * uniform(0.1, 0.5), 2)

                time += delay_time * delay_bool

                time = round(time, 2)

                sleep(time)

                patient_vehicle = "car"
                torgan_vehicle = "car"

                if urgent:
                    if patient_hospital.get_heliport() and destination_hospital.get_heliport():
                        patient_vehicle = "helicopter"
                    if torgan_hospital.get_heliport() and destination_hospital.get_heliport():
                        torgan_vehicle = "helicopter"

                print(f"\n{patient} arrived by {patient_vehicle} and {torgan} arrived by {torgan_vehicle} successfully at {destination_hospital} in {time} hours, including a delay of {delay_time * delay_bool} hours.\n")

                hospital_jid = str(destination_hospital.get_jid())
                send = True

            else:
                print(f"Message not recognized: MyJID:{self.agent.jid}; SenderJID:{msg.sender}, performative:{performative}")

            if send:
                transport_message = Message(to=hospital_jid)
                transport_message.body = jsonpickle.encode((torgan, torgan_hospital, patient))
                transport_message.set_metadata("performative", "confirm_transport")

                await self.send(transport_message)
        else:
            print(f"Agent {str(self.agent.jid)} did not received any message after 30 seconds")