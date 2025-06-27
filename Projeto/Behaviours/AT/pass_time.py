from random import randint
from spade.behaviour import PeriodicBehaviour

from Projeto.parameters import urgency_increase_chance

class PassTime(PeriodicBehaviour):
    async def run(self):
        for torgan, torgan_hospital in self.agent.torgan_tuple_list:
            if not torgan.getHOLD():
                old_time = torgan.getIschemiaTime()
                new_time = old_time - 1
                #print(f"PASS TIME: old={old_urgency}, new={new_urgency}")
                if new_time <= 0:
                    self.agent.torgan_tuple_list.remove((torgan, torgan_hospital))
                    print(f"{torgan} did not find a suitable patient in time.")
                else:
                    torgan.setIschemiaTime(new_time)

        for key in self.agent.patient_dic.keys():
            for patient in self.agent.patient_dic[key]:
                if not patient.getOrgan().getHOLD() and randint(1,100) <= urgency_increase_chance:
                    old_urgency = patient.getUrgency()
                    new_urgency = old_urgency - 1
                    #print(f"PASS TIME: old={old_urgency}, new={new_urgency}")
                    if new_urgency <= 0:
                        self.agent.patient_dic[key].remove(patient)
                        print(f"{patient} did not find a suitable organ in time and passed away...RIP")
                    else:
                        patient.setUrgency(new_urgency)