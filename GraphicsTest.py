import pyglet
import Render
import random

w = pyglet.window.Window(width=640, height=640, resizable=True)

r = Render.CubeCam(30)
r.setWindowSize(w.width, w.height)
r.setScale(10,10)

tot = 0
for i in range(-1, 2, 1):
    for j in range(-1, 2, 1):
        for k in range(-1, 2, 1):
            r.setPosition(tot, i, j, k)
            r.setColor(tot, i * 20, 128, j * 20)
            tot += 1

'''        
r.setPosition(0, 1, 0, 0)
r.setColor(0, 40, 128, 0)

r.setPosition(1, 8, -2, 1)
r.setColor(1, 40, 128, 80)
'''

'''for i in range(10):
    r.setPosition(i, random.randint(-5, 5), random.randint(-5, 5), random.randint(-5, 5))
    r.setColor(i, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))'''

c = 0
def randomize():
    global c
    c += 1
    if c % 5 == 0:
        for i in range(10):
            r.setPosition(i, random.randint(-5, 5), random.randint(-5, 5), random.randint(-5, 5))
            r.setColor(i, random.randint(0, 255), random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
@w.event
def on_draw():
    #randomize()
    r.draw()
pyglet.app.run()