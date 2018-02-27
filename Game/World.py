from Vectors import CardinalDirections
import Vectors
import RenderInterface as RI
from Log import print
from Blocks import BlockTypes, getModel, getTexture

import math
import numpy
import itertools
import noise

#World is a grid of tupels. The first value is the block, the second the damage done to the block.

class World:
    def xyAdjust(func):
        def wrap(self, x, y, z, *args):
            return func(self, *self.adjustPos(x, y, z), *args)
        return wrap
            
    def adjustPos(self, x, y, z):
        return x % self.size, y % self.size, z % self.height

    @xyAdjust
    def getBlockAt(self, x, y, z):
        return self.grid[x, y, z][0]
        
    def setBlockAt(self, x, y, z, block):
        self.grid[x, y, z] = (block, 0)
        
    def attackBlockAt(self, x, y, z, damage = 1):
        '''Deals damage to the block at the given position. Returns true if it has been destroyed,
        false otherwise.'''
        block = self.grid[x, y, z]
        damageTaken = block[1] + damage
        if damageTaken > block[0].health:
            self.grid[x, y, z] = (BlockTypes.AIR, 0)
            return block[0].drop
        self.grid[x, y, z] = (block[0], damageTaken)
        
    def coordinateValid(self, x, y, z):
        #A Coordinate is valid if it is greater equal 0 and lower than size
        return self.size > x >= 0 and self.size > y >= 0 and self.height > z >= 0
        
    def __init__(self, size, height):
        self.grid = numpy.array([[[(BlockTypes.WALL, 0) for i in range(size)] for j in range(height)] for j in range(size)])
        for x,z in itertools.product(range(size), range(size)):
            for y in range(height):
                h = (y - 1)/height
                if h < 0.05:
                    self.grid[x,y,z] = BlockTypes.WALL
                #if h > 2:
                    #self.grid[x,y,z] = BlockTypes.AIR
        self.size = size
        self.height = height

        print("Registering world blocks!")
        for x,y,z in itertools.product(range(size), range(height), range(size)):
            block = self.grid[x, y, z][0]
            id = RI.createObject()
            RI.setModel(id, getModel(block))
            TId = getTexture(block)
            RI.setTexture(id, TId)
            RI.move(id, (x,y,z))
            RI.setVisible(id, block.show)