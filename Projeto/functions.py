from math import sqrt

from Projeto.parameters import speed_hellichoppa, speed_car, urg_heli, max_start_urg

def priority_score(organ, hospital, patient):
    urg = patient.getUrgency() < max_start_urg * urg_heli

    time = calc_time(hospital, patient.hospital, urg)
    urg = patient.urgency

    time_max = organ.getIschemiaTime()

    if time >= 1.5*time_max:
       res = 'a'
    else:
        res = time + urg

    return res  #quanto menor o resultado, maior é a prioridade do processo

def blood_compatibility(organ, patient):

    ABO_pat = patient.organ.ABO
    Rh_pat = patient.organ.Rh
    ABO_org = organ.ABO
    Rh_org = organ.Rh

    if Rh_pat == "-" and Rh_org != "-":
        return False

    if ABO_pat == "A" and ABO_org not in "AO":
        return False

    if ABO_pat == "B" and ABO_org not in "BO":
        return False

    return True


def calc_time(h1, h2, urgent):
    x1 = h1.get_location().getX()
    y1 = h1.get_location().getY()
    x2 = h2.get_location().getX()
    y2 = h2.get_location().getY()

    dist = sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    speed = speed_car

    if urgent and h1.get_heliport and h2.get_heliport:
        speed = speed_hellichoppa

    travel_time = dist / speed

    return travel_time


def priority_neworgan(torgan, hospital, patient_list):
    result_list = []

    for patient in patient_list:
        if not patient.getOrgan().getHOLD():
            if blood_compatibility(torgan, patient):
                result_list.append(patient)
    try:
        result_list = sorted(result_list, key=lambda patient: priority_score(torgan, hospital, patient))

    except TypeError:
        pass

    if len(result_list) > 0:
        res = (torgan, hospital, result_list[0])
    else:
        res = (torgan, hospital, None)
    return res


def priority_newpatients(torgan_tuple_list, patient_dic):
    res = []

    for torgan_tuple in torgan_tuple_list:
        torgan, hospital = torgan_tuple

        if not torgan.getHOLD():
            patient_list = patient_dic[torgan.getName()]

            request = priority_neworgan(torgan, hospital, patient_list)

            torgan, hospital, patient = request

            if patient is not None:
                for p in patient_list:
                    if p.getID() == patient.getID():
                        p.getOrgan().setHOLD(True)

            res.append(request)

    return res

def three_way_time(h1, h2, dest, urgent):
    time1 = calc_time(h1, dest, urgent)
    time2 = calc_time(h2, dest, urgent)

    res = max(time1, time2)
    return res

def best_hospital_list(pat_hospital, organ_hospital, hospital_list, patient):
    urgent = patient.getUrgency() < max_start_urg * urg_heli
    result_list = sorted(hospital_list, key=lambda hospital: three_way_time(pat_hospital, organ_hospital, hospital, urgent))
    return result_list