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
# Stop     |  -1  | None             | Tells the rendering engine to terminate, terminating the game with it.
# RESERVED |  0   |                  | Reserved to mean that no instruction is there right now.
# Create   |  1   | OId              |
# Show     |  2   | (OId, True/False)|
#Initialize|  99  | None             | Called only once to tell the rendering that the game is now ready.
#These methods are called here and then translated to messages passed through the pipe to the rendering.
#initConnection MUST be called before any message can be passed.

#Right now, the validity of OId's is not checked.
#As long as you neither a) use a value not acquired with createObject and b) not use the value of a destroyed object, all should behave as expected.

import numpy as np

objectMap = np.array([])

def initConnection(pipe):
  '''Expects a Connection object leading to the process running the renderer.'''
  global out
  out = pipe
  out.send((99, None))

def createObject():
  '''Allocates and returns the lowest available ObjectId that can subsequently be used to identify an Object to the renderer.'''
  #This prevents that the number ever overflows, at the cost of a bit of performance with increasing objectcounts.
  #If this is ever a performance problem, collect free values in its own map. (Append destroyed values and the size of the array whenever a new Id is allocated.)
  global objectMap
  #If all values are used/True, append a new one and return its Id.
  if objectMap.all():
    objectMap = np.append(objectMap, [True])
    OId = len(objectMap) - 1 #New Id is the last element.
    out.send((1, (OId,)))
    return OId
  else:
    OId = np.argwhere(np.logical_not(objectMap))[0][0]
    objectMap[OId] = True
  return OId

def destroyObject(OId):
  '''Marks the given ObjectId as useable and hides whatever it was showing.'''
  objectMap[OId] = False
  show(OId, False)

def show(OId, show):
  '''Shows/Hides the Object referenced by the givne Id.'''
  out.send((2, (OId, show)))

def stop():
  out.send((-1, None))