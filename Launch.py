from Rendering.Main import render
from multiprocessing import Process, Queue
from time import sleep

def a():
  print("a")
  
def b():
  print("b")
  print("b")

inQueue = Queue()
outQueue = Queue()
rt = Process(target=render, args=(inQueue,outQueue))

if __name__ == '__main__':
  rt.start()
  inQueue.put(a)
  inQueue.put(b)
  inQueue.put(a)
  inQueue.put(False)
  outQueue.get(block=True)
  rt.join()
  print("Test successfull!")