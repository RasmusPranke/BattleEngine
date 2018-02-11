import os, importlib

for file in os.listdir():
  if file.endswith("Test.py"):
    importlib.import_module(file[0:len(file)-3])
  elif file.endswith(".py"):
    importlib.import_module(file[0:len(file)-3])