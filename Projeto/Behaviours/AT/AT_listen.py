import jsonpickle
from spade.behaviour import CyclicBehaviour

from Projeto.functions import priority_neworgan, priority_newpatients, best_hospital_list
from spade.message import Message
from Projeto.parameters import XMPP_SERVER, urg_thresh, max_start_urg

class ATListen(CyclicBehaviour):
    async def run(self):
        msg = await self.receive(timeout=10)
        if msg:

            performative = msg.get_metadata("performative")

            if performative == 'subscribe':
                hospital = jsonpickle.decode(msg.body)
                if hospital not in self.agent.hospital_list:
                    self.agent.hospital_list.append(hospital)


            elif performative == "subscribe_torgan": #informação de um orgão chega ao agente transplante

                torgan, hospital = jsonpickle.decode(msg.body)
                self.agent.torgan_tuple_list.append((torgan, hospital))
                print(f"\n{torgan} info received\n")

                #calcula o melhor paciente para o orgao que chegou se este existir

                patient_list = self.agent.patient_dic[torgan.getName()]
                torgan, hospital, patient = priority_neworgan(torgan, hospital, patient_list)

                if patient is not None:
                    id = patient.getID()
                    for patient_from_dic_list in self.agent.patient_dic[patient.getOrgan().getName()]:
                        if patient_from_dic_list.getID() == id:
                            patient_from_dic_list.getOrgan().setHOLD(True)

                    id = torgan.getID()
                    for torgan_from_list, hospital_from_list in self.agent.torgan_tuple_list:
                        if torgan_from_list.getID() == id:
                            torgan_from_list.setHOLD(True)

                    request_room = Message(to = "{}".format(patient.getHospital().get_jid()) )
                    request_room.body = jsonpickle.encode( (torgan, hospital, patient) )
                    request_room.set_metadata("performative", 'request_room')

                    self.agent.current_requests.append(request_room)

                else:
                    print(f"\nNo patient was found for {torgan} from {hospital}.\n")


            elif performative == "inform_patient_list":

                new_patients =  jsonpickle.decode(msg.body)

                for key, value in new_patients.items():
                    self.agent.patient_dic[key] += value

                for torgan, hospital, patient in priority_newpatients(self.agent.torgan_tuple_list, new_patients):

                    if patient is not None:
                        id = patient.getID()
                        for patient_from_dic_list in self.agent.patient_dic[patient.getOrgan().getName()]:
                            if patient_from_dic_list.getID() == id:
                                patient_from_dic_list.getOrgan().setHOLD(True)

                        id = torgan.getID()
                        for torgan_from_list, hospital_from_list in self.agent.torgan_tuple_list:
                            if torgan_from_list.getID() == id:
                                torgan_from_list.setHOLD(True)

                        request_room = Message(to = "{}".format(patient.getHospital().get_jid()))
                        request_room.body = jsonpickle.encode((torgan, hospital, patient))
                        request_room.set_metadata("performative", 'request_room')

                        self.agent.current_requests.append(request_room)
                    else:
                        print(f"\nNo patient was found for {torgan} from {hospital}.\n")

                string = "\nNew patients received\nCurrent waiting list:\n"

                for key, value in self.agent.patient_dic.items():
                    string += f"{key}:{len(value)} patients\n"

                print(string)

                # string = "\nNew patients received\nCurrent waiting list:\n"
                # for key, value in self.agent.patient_dic.items():
                #     string += f"{key}:\n"
                #     for patient in value:
                #         string += f"{patient}\n"
                #
                # print(string)


            elif performative == "confirm_room":

                torgan, hospital, patient = jsonpickle.decode(msg.body)

                tr_message = Message(to = "ATR@" + XMPP_SERVER)
                tr_message.body = msg.body
                tr_message.set_metadata("performative", "request_transport")

                await self.send(tr_message)

                print(f"\nConfirmation from {patient.getHospital()} for {patient}.\nInitiating transport for {torgan}...\n")


            elif performative == "refuse_room":

                torgan, hospital, patient = jsonpickle.decode(msg.body)

                urgency = patient.getUrgency()

                #nao foi encontrada sala e é possível transportar o paciente
                if urgency > max_start_urg * urg_thresh:
                    print(f'\nConditions not met for {patient} and {torgan} in {patient.getHospital()}.\nSearching for rooms in other hospitals...\n')

                    hospital_list = []

                    for hospital in self.agent.hospital_list:
                        if hospital.get_jid() != patient.getHospital().get_jid():
                            hospital_list.append(hospital)

                    result_list = best_hospital_list(patient.getHospital(), hospital, hospital_list, patient)
                    best_hospital = result_list[0]

                    request_another_room = Message(to="{}".format(best_hospital.get_jid()))
                    request_another_room.body = jsonpickle.encode((torgan, hospital, patient, result_list))
                    request_another_room.set_metadata("performative", 'request_another_room')

                    self.agent.current_requests.append(request_another_room)

                #nao foi encontrada sala, mas o paciente está em estado critico. nao é possível transportar o paciente
                else:

                    print(f'\nConditions not met for {patient} in {patient.getHospital()}.\nSearching for new patient for {torgan}...\n')

                    patient_list = self.agent.patient_dic[torgan.getName()]
                    id = patient.getID()


                    for patient_from_list in patient_list:
                        if patient_from_list.getID() == id or patient_from_list.getNoRoom():
                            patient_list.remove(patient_from_list)
                            patient_from_list.setNoRoom(True)

                    torgan, hospital, patient = priority_neworgan(torgan, hospital, patient_list)

                    if patient is not None:
                        id = patient.getID()
                        for patient_from_dic_list in self.agent.patient_dic[patient.getOrgan().getName()]:
                            if patient_from_dic_list.getID() == id:
                                patient_from_dic_list.getOrgan().setHOLD(True)

                        id = torgan.getID()
                        for torgan_from_list, hospital_from_list in self.agent.torgan_tuple_list:
                            if torgan_from_list.getID() == id:
                                torgan_from_list.setHOLD(True)

                        request_room = Message(to="{}".format(patient.getHospital().get_jid()))
                        request_room.body = jsonpickle.encode((torgan, hospital, patient))
                        request_room.set_metadata("performative", 'request_room')

                        self.agent.current_requests.append(request_room)

                    else:
                        print(f"\nNo patient was found for {torgan} from {hospital}.\n")


            elif performative == "confirm_another_room":
                torgan, hospital, patient, result_list = jsonpickle.decode(msg.body)

                tr_message = Message(to="ATR@" + XMPP_SERVER)
                tr_message.body = jsonpickle.encode((torgan, hospital, patient, result_list))
                tr_message.set_metadata("performative", "request_patient_transport")

                await self.send(tr_message)

                print(f"\nConditions met for {patient} and {torgan} at {hospital}.\nInitiating patient and organ transport...\n")


            elif performative == "refuse_another_room":
                torgan, hospital, patient, result_list = jsonpickle.decode(msg.body)

                result_list.pop(0)
                if len(result_list) > 0:
                    best_hospital = result_list[0]

                    request_another_room = Message(to="{}".format(best_hospital.get_jid()))
                    request_another_room.body = jsonpickle.encode((torgan, hospital, patient, result_list))
                    request_another_room.set_metadata("performative", 'request_another_room')

                    self.agent.current_requests.append(request_another_room)

                else:
                    for patient_from_list in self.agent.patient_dic[torgan.getName()]:
                        if patient_from_list.getID() == patient.getID():
                            patient_from_list.getOrgan().setHOLD(False)

                    for torgan_from_list, hospital_from_list in self.agent.torgan_tuple_list:
                        if torgan_from_list.getID() == torgan.getID():
                            torgan_from_list.setHOLD(False)

                    print(f"\nNo hospital with conditions met for {patient} and {torgan}\n")


            elif performative in ["confirm_op", "failure_op"]:
                if performative == "confirm_op":
                    torgan, hospital, patient = jsonpickle.decode(msg.body)

                    #torgan_tuple = (torgan, hospital)

                    torgan, hospital, patient = jsonpickle.decode(msg.body)
                    cond_torgan = False
                    i = 0

                    while not cond_torgan:
                        torgan_from_list, _ = self.agent.torgan_tuple_list[i]
                        if torgan.getID() == torgan_from_list.getID():
                            cond_torgan = True
                            self.agent.torgan_tuple_list.pop(i)
                        i += 1

                    cond_pat = False
                    i = 0
                    pat_list = self.agent.patient_dic[torgan.getName()]

                    while not cond_pat and i < len(pat_list):
                        patient_from_list = pat_list[i]
                        if patient.getID() == patient_from_list.getID():
                            cond_pat = True
                            self.agent.patient_dic[torgan.getName()].pop(i)
                        i += 1

                    print(f"\n{patient} procedure successful in {patient.getHospital()}!\n")

                elif performative == "failure_op":
                    kill_chart = jsonpickle.decode(msg.body)

                    hospital = kill_chart.getHospital()

                    organ = kill_chart.getOrgan()
                    organ_id = organ.getID()

                    patient = kill_chart.getPatient()
                    patient_id = patient.getID()

                    string = f"\nProcedure for {patient} and {organ} failure:\n"
                    if kill_chart.getKillOrgan():
                        string += f"Organ destroyed.\n"
                    if kill_chart.getKillPatient():
                        string += f"Patient died.\n"

                    print(string)

                    if kill_chart.getKillPatient():
                        cond_pat = False
                        i = 0
                        pat_list = self.agent.patient_dic[kill_chart.getPatient().getOrgan().getName()]

                        while not cond_pat and i < len(pat_list):
                            patient_from_list = pat_list[i]
                            if patient_id == patient_from_list.getID():
                                cond_pat = True
                                pat_list.pop(i)
                            i += 1

                    #se paciente nao morrer, tirar hold e mudar localização, para o caso de ele trocar de hospital e a operação correr mal na mesma
                    else:
                        for patient_from_list in self.agent.patient_dic[organ.getName()]:
                            if patient_from_list.getID() == patient_id:
                                patient_from_list.setHospital(hospital)
                                patient_from_list.getOrgan().setHOLD(False)


                    #se orgao for destruido
                    if kill_chart.getKillOrgan():
                        cond_torgan = False
                        i = 0

                        while not cond_torgan and i < len(self.agent.torgan_tuple_list):
                            torgan_from_list, _ = self.agent.torgan_tuple_list[i]
                            if organ_id == torgan_from_list.getID():
                                cond_torgan = True
                                self.agent.torgan_tuple_list.pop(i)
                            i += 1

                    #se orgao nao for destruido, tirar hold
                    else:
                        for organ_from_list, old_hospital in self.agent.torgan_tuple_list:
                            if organ_id == organ_from_list.getID():
                                self.agent.torgan_tuple_list.remove((organ_from_list, old_hospital))
                                organ.setHOLD(False)
                                self.agent.torgan_tuple_list.append((organ, hospital))

                    #calcular priority otv para todos pois foram tirados de hold orgaos e/ou pacientes
                    for patient_list in self.agent.patient_dic.keys():
                        for patient_from_list in self.agent.patient_dic[patient_list]:
                            if patient_from_list.getHospital().get_jid() == hospital.get_jid():
                                patient_from_list.setNoRoom(False)


                    for torgan, hospital, patient in priority_newpatients(self.agent.torgan_tuple_list, self.agent.patient_dic):

                        if patient is not None:
                            id = patient.getID()
                            for patient_from_dic_list in self.agent.patient_dic[patient.getOrgan().getName()]:
                                if patient_from_dic_list.getID() == id:
                                    patient_from_dic_list.getOrgan().setHOLD(True)

                            id = torgan.getID()
                            for torgan_from_list, hospital_from_list in self.agent.torgan_tuple_list:
                                if torgan_from_list.getID() == id:
                                    torgan_from_list.setHOLD(True)

                            request_room = Message(to = "{}".format(patient.getHospital().get_jid()) )
                            request_room.body = jsonpickle.encode( (torgan, hospital, patient) )
                            request_room.set_metadata("performative", 'request_room')

                            self.agent.current_requests.append(request_room)
                        else:
                            print(f"\nNo patient was found for organ: {torgan} from hospital: {hospital}.\n")

            elif performative == "failure_transport":
                torgan, _, patient = jsonpickle.decode(msg.body)

                for organ_from_list, hospital in self.agent.torgan_tuple_list:
                    if torgan.getID() == organ_from_list.getID():
                        self.agent.torgan_tuple_list.remove((organ_from_list, hospital))

                for patient_from_list in self.agent.patient_dic[torgan.getName()]:
                    if patient_from_list.getID() == patient.getID():
                        patient_from_list.getOrgan().setHOLD(False)

            else:
                print(f"Message not recognized: MyJID:{self.agent.jid}; SenderJID:{msg.sender}, performative:{performative}")

        else:
            print(f"Agent {str(self.agent.jid)} did not received any message after 10 seconds")