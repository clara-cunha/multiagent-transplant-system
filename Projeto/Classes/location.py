from random import randint

class Location:
    def __init__(self):
        self.x = randint(1, 100)
        self.y = randint(1, 100)

    def getX(self):
        return self.x

    def setX(self, x:int):
        self.x = x

    def getY(self):
        return self.y

    def setY(self, y:int):
        self.y = y

    def __str__(self):
        return "Location [X=" + str(self.x) + ", Y=" + str(self.y) + "]"