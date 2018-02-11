import os
import py_compile as pyc

targetDir = "x64/Debug/"

for file in os.listdir(targetDir):
  if file.endswith(".pyc"):
    os.remove(targetDir + file)

for file in os.listdir():
  if file.endswith(".py") and not file.endswith("Test.py") and file != "Compile.py" and file != "TestAll.py":
    pyc.compile(file, targetDir + file + "c", doraise = True)