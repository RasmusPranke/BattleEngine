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

class Game:

    def setActiveActor(self, actor):
        self.activeActor = actor

    def getActiveActor(self):
        return self.activeActor

    def run(self):
      
    def __init__(self, inPipe):        
        print("Creating World!")
        self.gameWorld = World(5, 4)
