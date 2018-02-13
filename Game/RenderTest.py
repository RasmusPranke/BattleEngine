import Render
from multiprocessing import Process, Pipe

class RenderInterfaceImpl:
  def __init__(self, renderRcvPipe):
    print("Creating impl! ", self)
    self.recvPipe = renderRcvPipe
    self.message = ()
    print(self.recvPipe)

  def loadMessage(self):
    if self.recvPipe.poll(1):
      message = self.recvPipe.recv()
      #Get the message Id, then set the message to be the arguments for the given messageId.
      ret = message[0]
      self.message = message[1]
      return ret
    #If no message is waiting, return -2 (to differentiate between an python cpp error and no message)
    return 0

  def getMessage(self):
    return self.message

def processFunction(interface):
  assert interface.loadMessage()
  msg = interface.getMessage() 
  print(msg)
  assert msg == "Hi there!"
  return

def test():
  print("Testing Pipe Thread Behaviour!")

  pipe = Pipe(False)
  process = Process(target=processFunction, args=(RenderInterfaceImpl(pipe[0]),))
  pipe[1].send((1, "Hi there!"))
  process.start()
  process.join()

  print("Done testing!")