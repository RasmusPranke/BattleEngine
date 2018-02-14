#Communication takes the following form:
#Each Object first accquires an ObjectId using createObject. This Id identifies the thing to modify to the rendering.
#Then, to have something to render, a ModelId must be accquired by using addModel(Model). This returns a ModelId, used for identifying this particular model.
#Finally, setModel(ObjectId, ModelId) attaches that Model to that Object, rendering it at the origin.
#Translate/Rotate(ObjectId, Vector) and Show(ObjectId, True/False) are used to move the Object and hide it if necessary.

#Operations are encoded as follows:
#(OpId, Argument)
#OpId is the operation id, as described in the table below.
#Argument is all information required by the renderer, encoded as a list of list of floating point values.

#Operation | OpId | Argument         | Comment
# RESERVED |  -1  |                  | Reserved for Engine internals. Don't use this as a message ID.
# Stop     |  0   | None             | Tells the rendering engine to terminate.
# Create   |  1   | None             | Returns an unused ObjectId and marks it as used.
# Destroy  |  2   | OId              | Frees the given OId to be reassigned later.
# Visible  |  3   | (OId, True/False)|
# Set Model|  4   | (OId, MId)       | Assigns the given Model to the given Object. Multiple Objects may share a Model.
# Model Operations
# Create   |  2   |[Model Points...] | Sends back the ID of the given Model.
#Initialize|  99  | None             | Called only once to tell the rendering that the game is now ready.
#These methods are called here and then translated to messages passed through the pipe to the rendering.
#initConnection MUST be called before any message can be passed.

#Right now, the validity of OId's is not checked.
#As long as you neither a) use a value not acquired with createObject and b) not use the value of a destroyed object, all should behave as expected.

import numpy as np
from multiprocessing import Process, Pipe

import Render

objectMap = np.array([])

class RenderInterfaceImpl:
  def __init__(self, renderRcvPipe):
    self.recvPipe = renderRcvPipe
    self.message = ()

  def loadMessage(self):
    if self.recvPipe.poll(1):
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
  render_gameSide.send((99, None))
  return userInput_gameSide

def createObject():
  '''Allocates and returns the lowest available ObjectId that can subsequently be used to identify an Object to the renderer.'''
  #This prevents that the number ever overflows, at the cost of a bit of performance with increasing objectcounts.
  #If this is ever a performance problem, collect free values in its own map. (Append destroyed values and the size of the array whenever a new Id is allocated.)
  #If all values are used/True, append a new one and return its Id.
  render_gameSide.send((1, None))
  print(render_gameSide.poll(20))
  return render_gameSide.recv()

def destroyObject(OId):
  '''Marks the given ObjectId as useable and hides whatever it was showing.'''
  render_gameSide.send((2, OId))

def setVisible(OId, show):
  '''Shows/Hides the Object referenced by the given Id.'''
  render_gameSide.send((3, (OId, show)))

def stop():
  render_gameSide.send((0, None))
  renderThread.join()