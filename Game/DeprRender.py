import SpecialMath as smath

import pyglet
import math

vertexList = None
allowedSquares = 0

sqrt3 = math.sqrt(3)

class gameSendlineCam:
    '''def __init__(self, maxCount \'''For how many blocks gameSendlines may be saved\'''):
        self.maxCount = maxCount
        self.'''

class WorldCam:
    def getIndex(self, x, y, z):
        index = 0
        
        #Calculate the layer
        tot = x + y + z 
        #In each layer, there are the sum from 1 to the layer blocks.
        #So, the first index of each layer is the sum of all those sums before it.
        index += smath.sumsum(tot)
        
        #Each of the total not in x determines part of the index
        #Each of those missing in y also determine the index.
        m = tot - x
        index += smath.sum(m) + y
        
        return index

    def __init__(self, xMax, yMax, zMax, world):
        '''Instantiates a cam that can display up to the given amount of Blocks in each direction.'''
        
class CubeRender:
    '''Defines a class for drawing up to the given amount of different cubes, viewed isometrically.'''
    
    def getCubeSize(self):
        '''Returns the side length of the cube in 3d space, streched for each dimension.'''
        cubeSizeX = self.windowX / self.cubesX
        cubeSizeY = self.windowY / self.cubesY
        return cubeSizeX, cubeSizeY
    
    def generateCubePoints(self, x = 0, y = 0):
        cubeSizeX, cubeSizeY = self.getCubeSize()
        r = 2 * cubeSizeX / sqrt3 #Horizontal radius of pointy-topped hexagon
        l = cubeSizeY #Vertical radius of pointy-topped hexagon.
        #The cube is centered so that the middle of the top face is at pixel position (x, y)
        
        points = []
        #Point order matters!
        
        #Upper Quad
        #Upper Point
        points.append(x)
        points.append(y + l/2)
        #Right Point
        points.append(x + r/2)
        points.append(y)
        #Down Point
        points.append(x)
        points.append(y - (l/2))
        #Left Point
        points.append(x - (r/2))
        points.append(y)
        
        #Right Quad
        #Upper Point
        points.append(x + r/2)
        points.append(y)
        #Right Point
        points.append(x + r/2)
        points.append(y - l)
        #Down Point
        points.append(x)
        points.append(y - (l/2) - l)
        #Left Point
        points.append(x)
        points.append(y - (l/2))
        
        #Left Quad
        #Upper Point
        points.append(x - (r/2))
        points.append(y)
        #Right Point
        points.append(x)
        points.append(y - (l/2))
        #Down Point
        points.append(x)
        points.append(y - (l/2) - l)
        #Left Point
        points.append(x - (r/2))
        points.append(y - l)
        
        return points
        
    
    def __init__(self, maxCount):
        self.maxCount = maxCount
        #A cube drawn isometrically is a set of 3 quads, which together form a hexagon.
        #As such, each cube requires 3 * 4 = 12 vertices for the sides, plus another 12 for the gameSendlines for better visibility.
        self.vertexMult = 3 * 4
        #Each Point of each quad requires 2 coordinates (x and y), so a total of 3*4*2 = 24 coordinates per cube.
        self.coordinateMult = self.vertexMult * 2
        #Each Quad requires one color per vertex, which is made up of 4 color values: RGBA. So, 3*4*4 = 48 color values per cube.
        self.colorMult = self.vertexMult * 4
        self.cubeList = pyglet.graphics.vertex_list(maxCount * self.vertexMult,
                                             ('v2f/stream', [0 for x in range(maxCount * self.coordinateMult)]),
                                             ('c4B/stream', [0 for x in range(maxCount * self.colorMult)]))
        self.gameSendlineList = pyglet.graphics.vertex_list(maxCount * self.vertexMult,
                                             ('v2f/stream', [0 for x in range(maxCount * self.coordinateMult)]),
                                             ('c4B/stream', [0 for x in range(maxCount * self.colorMult)]))
        self.xOff = 0
        self.yOff = 0
        self.windowX = 10
        self.windowY = 10
        self.cubesX = 1
        self.cubesY = 1
        
    def adjustAllPos(self, xAdjust, yAdjust):
        posList = self.cubeList.vertices[0:self.maxCount*self.coordinateMult]
        for i in range(len(posList)):
            if i % 2 == 0:
                posList[i] = xAdjust(posList[i])
            else:
                posList[i] = yAdjust(posList[i])
        self.cubeList.vertices = posList
        self.gameSendlineList.vertices = posList    
    
    def setOffset(self, x, y):
        '''The Vector from the middlemost cubes middle to the middle of the camera will be (x. y), where x and y are pixel values. This is equivalent to moving the camera by x, y.'''
        oldXOff = self.xOff
        oldYOff = self.yOff
        if oldXOff == x and oldYOff == y:
            return
        self.xOff = -x
        self.yOff = -y
        
        xAdjust = lambda x: x + self.xOff - oldXOff
        yAdjust = lambda y: y + self.yOff - oldYOff
        self.adjustAllPos(xAdjust, yAdjust)
        
    def setWindowSize(self, windowX, windowY):
        oldWindowX = self.windowX
        oldWindowY = self.windowY
        if oldWindowX == windowX and oldWindowY == windowY:
            return
        self.windowX = windowX
        self.windowY = windowY
        
        xAdjust = lambda x: (x / oldWindowX) * windowX
        yAdjust = lambda y: (y / oldWindowY) * windowY
        self.adjustAllPos(xAdjust, yAdjust)
        
    def setScale(self, cubesX, cubesY):
        '''Sets how many cubes should be visible along the x and the y axis.'''
        oldCubesX = self.cubesX
        oldCubesY = self.cubesY
        if oldCubesX == cubesX and oldCubesY == cubesY:
            return
        self.cubesX = cubesX
        self.cubesY = cubesY
        
        xAdjust = lambda x: (x / oldCubesX) * cubesX
        yAdjust = lambda y: (y / oldCubesY) * cubesY
        self.adjustAllPos(xAdjust, yAdjust)
        
    def cubeToScreenSpace(self, x, y, z):
        '''Calculates the center point on screen of a cube at (x, y, z).'''
        cubeSizeX, cubeSizeY = self.getCubeSize()
        
        xPixPerX = (cubeSizeX) / (sqrt3)
        xPixPerY = -(cubeSizeY) / (sqrt3)
        xPixPerZ = 0
        
        yPixPerX = cubeSizeX / 2
        yPixPerY = cubeSizeY / 2
        yPixPerZ = cubeSizeY
        
        xPix = xPixPerX * x + xPixPerY * y + xPixPerZ * z
        yPix = yPixPerX * x + yPixPerY * y + yPixPerZ * z
        return xPix, yPix
 
    def screenToCubeSpace():
        '''To be implemented.'''
        pass
        
    def setPosition(self, index, x, y, z):
        '''Sets the position of the given Index at cube space (x, y, z).'''
        x, y = self.cubeToScreenSpace(x, y, z)
        
        newPosList = self.generateCubePoints(x, y)
        basePos = index * self.coordinateMult
        self.cubeList.vertices[basePos:basePos + self.coordinateMult] = newPosList
        self.gameSendlineList.vertices[basePos:basePos + self.coordinateMult] = newPosList
            
    def setColor(self, index, r,g,b, a=255):
        basePos = index * self.colorMult
        #For each vertex per cube, replace its color values with the new rgba
        self.cubeList.colors[basePos:basePos + self.colorMult] = ([r,g,b,a] * self.vertexMult)

    def draw(self):
        if self.cubeList is not None:
            self.cubeList.draw(pyglet.gl.GL_QUADS)
            #self.cubeList.draw(pyglet.gl.QUAD_STRIP)
        else:
            print("Cube List not yet initialized!")
        if self.gameSendlineList is not None:
            pass
            #self.gameSendlineList.draw(pyglet.gl.GL_LINES)
        else:
            print("gameSendline List not yet initialized!")

def init(squareCount):
    global vertexList
    vertexList = pyglet.graphics.vertex_list(squareCount * 4,
                                             ('v2f/stream', [0 for x in range(squareCount * 8)]),
                                             ('c4B/stream', [0 for x in range(squareCount * 16)]))

def setSquarePos(index, x, y, xSize, ySize):
    vertexList.vertices[index*8:index*8 + 8] = [
        x, y,
        x + xSize, y,
        x + xSize, y + ySize,
        x, y + ySize
        ]

def setSquareColor(index, red, green, blue, alpha = 255):
    vertexList.colors[index*16:index*16 + 16] = [
        red,
        green,
        blue,
        alpha,
        red,
        green,
        blue,
        alpha,
        red,
        green,
        blue,
        alpha,
        red,
        green,
        blue,
        alpha
        ]

def setSquare(index, x, y, xSize, ySize, red=0, blue=0, green=0, alpha=255):
    setSquarePos(index, x, y, xSize, ySize)
    setSquareColor(index, red, green, blue, alpha)

def draw():
    if vertexList is not None:
        vertexList.draw(pyglet.gl.GL_QUADS)
    else:
        print("Vertex List not yet initialized!")
