#Log Console output to file

import datetime
import sys
import os

'''Defines a print function which:
   - Outputs to the terminal
   - Appends to a file with the datetime of execution as the filename
   - This file is put in a subfolder log created in the execution directory.'''

time = datetime.datetime.now()
file_name = time.strftime("%y-%m-%d-%H-%M-%S")

printO = print

def print(*args, **kwargs):
    if not os.path.exists("log/"):
        os.makedirs("log/")
    orig_stdout = sys.stdout

    f = open('log/'+file_name+'.log', 'a')

    sys.stdout = f
    printO(*args, **kwargs) #print to file
    f.close()

    sys.stdout = orig_stdout
    printO(*args, **kwargs) #print to console