def render(inQueue, outQueue):
  observation = inQueue.get(block=True)
  while(observation):
    observation()
    observation = inQueue.get(block=True)
  outQueue.put(True)