from spade import agent

from Projeto.Behaviours.ATR.ATR_listen import ATRListen

class ATR(agent.Agent):

    async def setup(self):
        print("\nATR starting...\n")

        a = ATRListen()
        self.add_behaviour(a)