import itertools
from numpy import random
import math
from enum import Enum

from World import World
from Actor import Actor
from Blocks import BlockTypes
from Log import print
import GameToRenderInterface as GTRI

def start(myOutPipe, myInPipe):
  print("Starting!")
  GTRI.initConnection(myOutPipe)
  game = Game(myInPipe)
  game.run()

#By adding key-function pairs to the actionlist, button functions
#    can easily be modified at runtime

class Modes(Enum):
    def cubeDraw(game, window):
        count = 0
        mul = game.getGraphicsSizeMul()
    
        #Hardcoded, change this!
        game.cubeCam.setScale(10, 10)
        game.cubeCam.setWindowSize(window.width, window.height)
        game.cubeCam.setOffset(0, 0)
    
        for i in itertools.product(range(game.gameWorld.size), range(game.gameWorld.size), range(game.gameWorld.height)):
            game.cubeCam.setPosition(count, *i)
            game.cubeCam.setColor(count, *game.gameWorld.getBlockAt(*i).color)
            count = count + 1
        
        '''for a in game.actors:
            Render.setSquarePos(count, *[a*b + 0.325 * b for a,b in zip(a.getPos(),mul)], *[0.35*a for a in mul])
            Render.setSquareColor(count, *a.getColor())
            count = count + 1'''
        
        game.cubeCam.draw()

    def GAMEupdate(game, dt):
        for ac in game.actors:
            ac.act()
        


    GAME = (1, cubeDraw, GAMEupdate)

    def __init__(self, id, drawMethod, updateMethod):
        self.id = id
        self.drawMethod = drawMethod
        self.updateMethod = updateMethod
       

class Game:

    actionList = {
    }

    activeActor = None

    def setActiveActor(self, actor):
        self.activeActor = actor

    def getActiveActor(self):
        return self.activeActor

    def parseMousePos(self, pos):
        mul = self.getGraphicsSizeMul()
        return [(int) (a/b) for a,b in zip(pos, mul)]

    #Move this to mode selection
    def addPlayKeys(self, list):
        def move(vector):
            pos = getActiveActor().getPos()
            getActiveActor().appendTarget(*[a+b for a,b in zip(pos, vector)])

        list[pyglet.window.key.UP] = lambda mod: move((0, 1))
        list[pyglet.window.key.DOWN] = lambda mod: move((0, -1))
        list[pyglet.window.key.LEFT] = lambda mod: move((-1, 0))
        list[pyglet.window.key.RIGHT] = lambda mod: move((1, 0))
        
    def getGraphicsSizeMul():
        pass
    
    def drawGame(self):
        pass

    def update(dt):
        pass

    def reset(self):
        def fpass(self): pass
        self.drawGame = fpass
        self.update = fpass

    def setMode(self, mode):
        self.reset()
        print(mode)
        self.drawGame = mode.drawMethod
        self.update = mode.updateMethod

    def run(self):
      pass
      #GTRI.stop()

    def __init__(self, inPipe):
        self.actionList = {}
        
        print("Creating World!")
        self.gameWorld = World(5, 3)
