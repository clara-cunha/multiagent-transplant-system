from spade import quit_spade
from time import sleep
from Projeto.Agents.AH import AH
from Projeto.Agents.AT import AT
from Projeto.Agents.AR import AR
from Projeto.Agents.ATR import ATR
from Projeto.parameters import XMPP_SERVER, PASSWORD, hospital_number

if __name__ == '__main__':

    AT_jid = 'AT@' + XMPP_SERVER
    AR_jid = 'AR@' + XMPP_SERVER
    ATR_jid = 'ATR@' + XMPP_SERVER

    AR_agent = AR(AR_jid, PASSWORD)
    AT_agent = AT(AT_jid, PASSWORD)
    ATR_agent = ATR(ATR_jid, PASSWORD)

    res_AT = AT_agent.start(auto_register=True)
    res_AT.result()
    res_AR = AR_agent.start(auto_register = True)
    res_AR.result()

    res_ATR = ATR_agent.start(auto_register = True)
    res_ATR.result()

    hospital_agent_list = []

    for i in range(1,hospital_number + 1):
        AH_jid = 'AH' + str(i) + '@' + XMPP_SERVER
        AH_agent = AH(AH_jid, PASSWORD)
        res_AH = AH_agent.start(auto_register=True)
        res_AH.result()
        hospital_agent_list.append(AH_agent)


    print('agentes results')

    while AR_agent.is_alive() and AT_agent.is_alive() and ATR_agent.is_alive():
        try:
            sleep(1)
        except KeyboardInterrupt:
            AR_agent.stop()
            AT_agent.stop()
            ATR_agent.stop()

            for agent in hospital_agent_list:
                agent.stop()

            break
    print('END')

    quit_spade()