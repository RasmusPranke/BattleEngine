import numpy as np
from multiprocessing import Process, Pipe
import math

import Render

objectMap = np.array([])

class RenderInterfaceImpl:
  def __init__(self, renderRcvPipe):
    self.recvPipe = renderRcvPipe
    self.message = ()

  def loadMessage(self):
    if self.recvPipe.poll():
      message = self.recvPipe.recv()
      #Get the message Id, then set the message to be the arguments for the given messageId.
      ret = message[0]
      self.message = message[1]
      return ret
    #If no message is waiting, return -2 (to differentiate between an python cpp error and no message)
    return -2

  def getMessage(self):
    return self.message

  def sendMessage(self, msg):
    self.recvPipe.send(msg)

'''Set up the rendering process.'''
inputPipe = Pipe(False)
renderPipe = Pipe(True)

userInput_gameSide = inputPipe[0]
render_gameSide = renderPipe[1]
render_renderSide = renderPipe[0]
userInput_renderSide = renderPipe[1]

renderThread = Process(target=Render.start,
                        args=((RenderInterfaceImpl(render_renderSide),)))#, '''renderSend'''),))

def initilaizeRender():
  '''Spawn the new Process.'''
  renderThread.start()
  return userInput_gameSide

def createObject():
  '''Allocates and returns the lowest available ObjectId that can subsequently be used to identify an Object to the renderer.'''
  #This prevents that the number ever overflows, at the cost of a bit of performance with increasing objectcounts.
  #If this is ever a performance problem, collect free values in its own map. (Append destroyed values and the size of the array whenever a new Id is allocated.)
  #If all values are used/True, append a new one and return its Id.
  render_gameSide.send((1, None))
  return render_gameSide.recv()

def destroyObject(OId):
  '''Marks the given ObjectId as useable and hides whatever it was showing.'''
  render_gameSide.send((2, OId))

def setVisible(OId, show):
  '''Shows/Hides the Object referenced by the given Id.'''
  render_gameSide.send((3, (OId, show)))

def setModel(OId, MId):
  render_gameSide.send((4, (OId, MId)))

def createModel(model):
  if not isinstance(model, str):
    model = [x for x in model]
    render_gameSide.send((11, model))
  else:
    raise NameError("File loading not yet implemented!")
  re = render_gameSide.recv()
  return re

def createTexture(MId, texture):
  if not isinstance(texture, str):
    texture = [x for x in texture]
    render_gameSide.send((31, (MId, texture)))
  else:
    raise NameError("File loading not yet implemented!")
  re = render_gameSide.recv()
  return re

def setTexture(OId, TId):
    render_gameSide.send((8, (OId, TId)))

def move(OId, vector):
    '''Moves OId by Vector.
       Expects any object with vaild numbers accessible via indices 0-2 as vector.'''
    render_gameSide.send((5, (OId, (vector[0],vector[1],vector[2]))))

def rotate(OId, vector, amount):
    render_gameSide.send((6, (OId, (vector[0],vector[1],vector[2]), amount)))

def scale(OId, vector):
    '''Scales OId by Vector.
       Expects any object with vaild numbers accessible via indices 0-2 as vector.'''
    render_gameSide.send((7, (OId, (vector[0],vector[1],vector[2]))))
    
def moveCam(vector):
    '''Moves OId by Vector.
       Expects any object with vaild numbers accessible via indices 0-2 as vector.'''
    render_gameSide.send((25, (0, (vector[0],vector[1],vector[2]))))

def setCam(vector):
    '''Moves OId by Vector.
       Expects any object with vaild numbers accessible via indices 0-2 as vector.'''
    render_gameSide.send((29, (0, (vector[0],vector[1],vector[2]))))

def rotateCam(vector, amount):
    render_gameSide.send((26, (0, (vector[0],vector[1],vector[2]), amount*2*math.pi)))

def pivotCam(vector, amount):
    render_gameSide.send((28, (0, (vector[0],vector[1],vector[2]), amount*2*math.pi)))

def lookAt(vector):
    render_gameSide.send((27, (0, (vector[0],vector[1],vector[2]))))

def stop():
  render_gameSide.send((0, None))
  renderThread.join()