import time as Time

enabled = False
timers = {}

def startTimer(operation):
    '''Starts the timer for the given operation from 0. Operation may be any immutable type.'''
    timers[operation] = Time.time()

def time(operation):
    '''Prints out the time since the timer for the given operation has been started and returns that number. Operation may be any immutable type.'''
    if operation in timers:
        t = Time.time() - timers[operation]
        print(operation, " took ", t)
        del timers[operation]
        return t