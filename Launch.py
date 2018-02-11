from multiprocessing import Process, Pipe
from Game import start

import sys
sys.argv = ["F- off"]

renderToGame = Pipe(False)
gameToRender = Pipe(False)

gameRecieve = renderToGame[0]
gameSend = gameToRender[1]
renderRecieve = gameToRender[0]
renderSend = renderToGame[1]

gameThread = Process(target=start, args=(gameSend,gameRecieve))
#Starting the new Thread causes BS, probably by launching the application itself anew.
message = (0,)

def launch():
  gameThread.start()
  pass

def loadMessage():
  if not renderRecieve.poll():
    return 0
  else:
    global message
    message = renderRecieve.recv()
    #Get the message Id, then set the message to be the arguments for the given messageId.
    ret = message[0]
    message = message[1]
    return ret

def getMessage():
  return message

def exit():
  print("Shutting down game!")
  renderSend.put(False)
  gameThread.join()