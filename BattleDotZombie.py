import RenderInterface as RI
import Game

def exit():
  print("Shutting down game!")
  RI.stop()

if __name__ == "__main__":
  #from RenderTest import test
  #test()
  pipe = RI.initilaizeRender()
  Game.start(pipe)
  exit()