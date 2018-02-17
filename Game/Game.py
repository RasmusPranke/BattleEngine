import itertools
from numpy import random
import math
from enum import Enum

from World import World
from Actor import Actor
from Log import print
import RenderInterface as RI

def start(myInPipe):
  print("Starting!")
  game = Game(myInPipe)
  game.run()
  RI.stop()

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
      rand = random.random
      def r():
          return (rand() * 2) - 1
      
      #Creates a square.
      #model = [1,1,0,1,-1,0,-1,1,0,
      #         -1,-1,0,1,-1,0,-1,1,0]
      #modelId = RI.createModel(model)
      #id = RI.createObject()
      #RI.setModel(id, modelId)
      #RI.setVisible(id, True)
      ''' #Creates random triangles
      for i in range(10):
        model = [r(), r(),r(),r(), r(),r(),r(), r(),r(),r(), r(),r(),r(), r(),r(),r(), r(),r(),r(), r(),r(),r(), r(),r(),r(), r(),r(),r(), r(),r(),r(), r(),r(),r(), r(),r()]
        modelId = RI.createModel(model)
        RI.setModel(id, modelId)
        RI.setVisible(id, True)
        input("Press Enter to continue...")
      for i in range(10):
        input("Press Enter to continue...")
        RI.rotateCam((0,1,0), 0.25)
      '''
      RI.moveCam((0,0,-5))
      while True:
        input("Press Enter to continue...")
        RI.rotateCam((0, 1, 0), 0.2)
      
    def __init__(self, inPipe):
        self.actionList = {}
        
        print("Creating World!")
        self.gameWorld = World(5, 3)
