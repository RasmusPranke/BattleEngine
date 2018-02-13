import RenderInterface as GTRI
from numpy import random as rng
from multiprocessing import Pipe

connection = Pipe(False)
recieving = connection[0]

def assertMessageEqual(thing):
  '''Asserts both whether the connection is fast enough and whether its return is equal to thing.'''
  assert recieving.poll(0.03)
  assert recieving.recv() == thing

GTRI.initConnection(connection[1])
assertMessageEqual((99, None))

testCases = 1000

for i in range(testCases):
  #Id's should count up from 0
  assert GTRI.createObject() == i
  assertMessageEqual((1, (i,)))

freedIds = []
for _ in range(100):
  #Test whether removing a random element actually frees its Id.
  i = rng.randint(testCases)
  while i in freedIds:
    i = rng.randint(testCases)

  GTRI.destroyObject(i)
  freedIds.append(i)
  #Destroying an object should send a show message.
  assertMessageEqual((2, (i, False)))

#All previously destroyed Id's should be restored in ascending order.
#This should not send any message
freedIds.sort()
for i in freedIds:
  OId = GTRI.createObject()
  assert i == OId
  assert not recieving.poll(0.03)

recieving.close()