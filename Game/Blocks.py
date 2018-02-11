from Items import ItemTypes

from enum import Enum
import math

class BlockTypes(Enum):
    AIR = (True, [0, 0, 0, 0], 0)
    GRASS = (False, [0, 128, 0], 1, (ItemTypes.SEED, 1))
    WALL = (False, [128, 128, 128], 10, (ItemTypes.STONE, 1))

    def __init__(self, passable = False, color = [0, 0, 0, 255], health = math.inf, drop = (None, 1)):
        self.passable = passable
        self.color = color
        self.health = health
        self.drop = drop
        
    def isPassable(self):
        return self.passable
        
    def getColor(self):
        return self.color