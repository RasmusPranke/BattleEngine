import pyglet
import itertools
import random
import math
from enum import Enum

from World import World
from Actor import Actor
from Blocks import BlockTypes
import Render

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
        

    def __init__(self, gridSize):
        self.actionList = {}

        self.gameWorld = World(gridSize, 3)
        player = Actor(self.gameWorld)
        self.actors = [player]
        self.setActiveActor(player)
    
        window = pyglet.window.Window(resizable=True)
        self.cubeCam = Render.CubeCam(gridSize * gridSize * 3)
        #Render.init(gridSize * gridSize + len(self.actors))
    
        self.addPlayKeys(self.actionList)

        def getGraphicsSizeMul():
            return [window.width / gridSize, window.height / gridSize]
        self.getGraphicsSizeMul = getGraphicsSizeMul

        @window.event
        def on_draw():
            self.drawGame(self, window)
        
        @window.event
        def on_key_press(symbol, modifiers):
            if symbol in self.actionList:
                self.actionList[symbol](modifiers)
        
        @window.event
        def on_mouse_press(x, y, button, modifiers):
            if button == pyglet.window.mouse.RIGHT:
                z = 0
                if modifiers & pyglet.window.key.MOD_SHIFT:
                    z = 1
                elif modifiers & pyglet.window.key.MOD_CTRL:
                    z = -1
                args = (*self.parseMousePos((x,y)), z)
                player.setTarget(*args)
            if button == pyglet.window.mouse.LEFT:
                x, y = self.parseMousePos((x, y))
                z = 0
                if self.gameWorld.getBlockAt(x,y,z) == BlockTypes.GRASS:
                    self.gameWorld.setBlockAt(x, y, z, BlockTypes.WALL)
                else:
                    self.gameWorld.setBlockAt(x, y, z, BlockTypes.GRASS)
        def moveRand(dt):
            vector = [0, 0]
            if random.random() > 0.5:
                vector = [1, 0]
            else:
                vector = [0, 1]
            player.appendTarget(*[a+b for a,b in zip(vector, player.getPos())])
        
        def update(dt):
            self.update(self, dt)
        
        #pyglet.clock.schedule_interval(moveRand, 0.5)
        pyglet.clock.schedule_interval(update, 0.5)
    
        self.setMode(Modes.GAME)
        pyglet.app.run()
