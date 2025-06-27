import random
from Projeto.Classes.location import Location
from Projeto.parameters import heliport_chance


class Hospital:
    def __init__(self, jid:str):
        self.location = Location()
        self.jid = jid
        self.heliport = False
        if random.randint(1,100) < heliport_chance:
            self.heliport = True

    def get_location(self):
        return self.location

    def get_jid(self):
        return self.jid

    def get_heliport(self):
        return self.heliport

    def set_heliport(self, heliport):
        self.heliport = heliport

    def __str__(self):
        return f'Hospital {self.jid[2:self.jid.index("@")]} at {self.location}'