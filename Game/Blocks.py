from Items import ItemTypes
import RenderInterface as RI

from enum import Enum
import math

blockModel = (#Front
-0.5,0.5,-0.5, -0.5,-0.5,-0.5, 0.5,0.5,-0.5,
0.5,0.5,-0.5, -0.5,-0.5,-0.5, 0.5,-0.5,-0.5,
#Back
0.5,0.5,0.5, -0.5,-0.5,0.5, -0.5,0.5,0.5,
0.5,-0.5,0.5, -0.5,-0.5,0.5, 0.5,0.5,0.5,
#Left
-0.5,-0.5,-0.5, -0.5,0.5,-0.5, -0.5,0.5,0.5,
-0.5,0.5,0.5, -0.5,-0.5,0.5, -0.5,-0.5,-0.5,
#Right
0.5,0.5,0.5, 0.5,0.5,-0.5, 0.5,-0.5,-0.5,
0.5,-0.5,-0.5, 0.5,-0.5,0.5, 0.5,0.5,0.5,
#Top
-0.5,0.5,0.5, -0.5,0.5,-0.5, 0.5,0.5,-0.5,
0.5,0.5,-0.5, 0.5,0.5,0.5, -0.5,0.5,0.5,
#Bottom
0.5,-0.5,0.5, -0.5,-0.5,-0.5, -0.5,-0.5,-0.5,
-0.5,-0.5,0.5, 0.5,-0.5,0.5, 0.5,-0.5,-0.5)

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

def showBlock(block, oid):
    RI.setModel(oid, getModel(block))
    RI.setTexture(oid, getTexture(block))
    RI.setVisible(oid, block.show)

    
class BlockTypes(Enum):
    AIR = (True, (1, 1, 1), False, 0)
    GRASS = (False, (0, 0.75, 0), True, 1, (ItemTypes.SEED, 1))
    WALL = (False, (0.5, 0.5, 0.5), True, 10, (ItemTypes.STONE, 1))
    MUSTARDGAS = (False, (1, 1, 0), True, 10, (ItemTypes.STONE, 1))
    IRONORE = (False, (0.8, 0.1, 0.1), True, 10, (ItemTypes.STONE, 1))
    WOOD = (False, (0.7, 0.3, 0.0), True, 10, (ItemTypes.STONE, 1))

    def __init__(self, passable = False, color = (0, 0, 0), show = True, health = math.inf, drop = (None, 1)):
        self.passable = passable
        self.color = color * (int)(len(blockModel) / 3)
        self.show = show
        self.model = blockModel
        self.health = health
        self.drop = drop

    def isPassable(self):
        return self.passable
        
    def getColor(self):
        return self.color