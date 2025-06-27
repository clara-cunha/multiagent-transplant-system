#Server Parameters

XMPP_SERVER = "your_server"
PASSWORD = "your_password"

#Organ Parameters

#ischemia_time -> hours
organ_type_dic = {
                    'kidney': {'ischemia_time' : 24, 'op_time' : 4, 'op_kill_organ' : 7, 'op_kill_patient' : 2},
                    'heart' : {'ischemia_time' : 4, 'op_time' : 4, 'op_kill_organ' : 20, 'op_kill_patient' : 20},
                    'liver' : {'ischemia_time' : 8, 'op_time' : 9, 'op_kill_organ' : 2, 'op_kill_patient' : 4},
                    'lung' : {'ischemia_time' : 4, 'op_time' : 5, 'op_kill_organ' : 15, 'op_kill_patient' : 5},
                    'cornea' : {'ischemia_time' : 168, 'op_time' : 1, 'op_kill_organ' : 30, 'op_kill_patient' : 1},
                    'pancreas' : {'ischemia_time' : 12, 'op_time' : 6, 'op_kill_organ' : 5, 'op_kill_patient' : 3}
                  }

ABO = ['A', 'B', 'AB', 'O']
RH = ['+', '-']

# organ_type_dic = {'orgao_teste':{'ischemia_time' : 24, 'op_time' : 20,'op_kill_organ' : 50, 'op_kill_patient' : 50}}
# ABO = ['A']

#Transport Parameters

speed_hellichoppa = 200
speed_car = 80

failure_rate = 10
delay_rate = 50


## Hospital Parameters
hospital_number = 15

min_rooms = 5
max_rooms = 10

min_teams = 5
max_teams = 10

min_pat_period = 1
max_pat_period = 5

min_org_period = 7
max_org_period = 10

heliport_chance = 70


#Patient Parameters

min_start_urg = 5
max_start_urg = 10

urgency_increase_chance = 10

urg_heli = 0.5 #percentagem de urgencia maxima: urgencia a partir da qual é considerado urgente e vai de helicoptero
urg_thresh = 0.2 #percentagem de urgencia maxima: urg a partir da qual pode ser movido