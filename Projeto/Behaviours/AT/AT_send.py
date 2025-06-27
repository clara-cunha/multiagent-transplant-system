from spade.behaviour import CyclicBehaviour

class ATSend(CyclicBehaviour):
    async def run(self):
        if len(self.agent.current_requests) > 0:
            await self.send(self.agent.current_requests[0])
            self.agent.current_requests.pop(0)