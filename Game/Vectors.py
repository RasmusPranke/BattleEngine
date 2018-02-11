from enum import Enum
import math

cardinalMap = {}

class CardinalDirections(Enum):
    NORTH = (0, 1, 0)
    SOUTH = (0, -1, 0)
    EAST = (1, 0, 0)
    WEST = (-1, 0, 0)
    
    NORTHUP = (0, 1, 1)
    SOUTHUP = (0, -1, 1)
    EASTUP = (1, 0, 1)
    WESTUP = (-1, 0, 1)
    
    NORTHDOWN = (0, 1, -1)
    SOUTHDOWN = (0, -1, -1)
    EASTDOWN = (1, 0, -1)
    WESTDOWN = (-1, 0, -1)
    
    INVALID = (0, 0, 0)
    
    def __init__(self, x, y, z):
        cardinalMap[(x, y, z)] = self
        self.x = x
        self.y = y
        self.z = z
        
def getCardinalDirection(x, y, z):
    '''Returns the CardinalDirection which most closely matches the given Vector, preferring the vertical axis if neither argument is larger. (0, 0) returns CardinalDirections.INVALID'''
    if y == 0 and x == 0:
        return CardinalDirections.INVALID
    if abs(x) > abs(y):
        x = abs(x) / x
        y = 0
    else:
        x = 0
        y = abs(y) / y
        
    if z != 0:
        z = abs(z)/z
    
    return cardinalMap[(x, y, z)]
    
def stepDistance(fromX, fromY, fromZ, toX, toY, toZ):
    return math.sqrt(abs(toX - fromX) + abs(toY - fromY) + abs(toZ - fromZ))
    
def euclideanDistance(fromX, fromY, fromZ, toX, toY, toZ):
    return abs(toX - fromX) + abs(toY - fromY) + abs(toZ - fromZ)
    