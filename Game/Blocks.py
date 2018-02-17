from Items import ItemTypes
import RenderInterface as RI

from enum import Enum
import math

blockModel = (-1.0,-1.0,-1.0,
              -1.0,-1.0, 1.0,
              -1.0, 1.0, 1.0, 
               1.0, 1.0,-1.0, 
              -1.0,-1.0,-1.0,
              -1.0, 1.0,-1.0,

               1.0,-1.0, 1.0,
              -1.0,-1.0,-1.0,
               1.0,-1.0,-1.0,
               1.0, 1.0,-1.0,
               1.0,-1.0,-1.0,
              -1.0,-1.0,-1.0,

              -1.0,-1.0,-1.0,
              -1.0, 1.0, 1.0,
              -1.0, 1.0,-1.0,
               1.0,-1.0, 1.0,
              -1.0,-1.0, 1.0,
              -1.0,-1.0,-1.0,

              -1.0, 1.0, 1.0,
              -1.0,-1.0, 1.0,
               1.0,-1.0, 1.0,
               1.0, 1.0, 1.0,
               1.0,-1.0,-1.0,
               1.0, 1.0,-1.0,

               1.0,-1.0,-1.0,
               1.0, 1.0, 1.0,
               1.0,-1.0, 1.0,
               1.0, 1.0, 1.0,
               1.0, 1.0,-1.0,
              -1.0, 1.0,-1.0,

               1.0, 1.0, 1.0,
              -1.0, 1.0,-1.0,
              -1.0, 1.0, 1.0,
               1.0, 1.0, 1.0,
              -1.0, 1.0, 1.0,
               1.0,-1.0, 1.0)

modelMap = {}
textureMap = {}

def getModel(block):
    if not repr(block) in modelMap:
        modelMap[repr(block)] = RI.createModel(block.model)
    return modelMap[repr(block)]

def getTexture(block):
    if not repr(block) in textureMap:
        textureMap[repr(block)] = RI.createTexture(getModel(block), block.color)
    return textureMap[repr(block)]
    
class BlockTypes(Enum):
    AIR = (True, (1, 1, 1), 0)
    GRASS = (False, (1, 1, 1), 1, (ItemTypes.SEED, 1))
    WALL = (False, (1, 1, 1), 10, (ItemTypes.STONE, 1))

    def __init__(self, passable = False, color = (0, 0, 0), health = math.inf, drop = (None, 1)):
        self.passable = passable
        self.color = color * (int)(len(blockModel) / 3)
        self.model = blockModel
        self.health = health
        self.drop = drop

    def isPassable(self):
        return self.passable
        
    def getColor(self):
        return self.color