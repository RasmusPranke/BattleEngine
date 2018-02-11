from Inventory import Inventory
import Vectors
from Vectors import CardinalDirections

import itertools
import math

INVENTORY_SIZE_CONST = 5

class Actor:
    def cardinalToXYZ(self, cardinal):
        return self.x + cardinal.x, self.y + cardinal.y, self.z + cardinal.z

    def __init__(self, world):
        self.world = world
        self.x, self.y, self.z = 0, 0, 0
        
        self.targets = []
        self.currentTarget = (0, 0, 0)
        self.path = [] #path is a list of cardinals to follow to the target
        
        self.inventory = Inventory(INVENTORY_SIZE_CONST)
        
    def getPos(self):
        return self.x, self.y, self.z
        
    def getColor(self):
        return [128, 55, 55]
        
    def move(self, cardinal):
        '''Returns whether this actor successfully moved along the cardinal'''
        x, y, z = self.cardinalToXYZ(cardinal)
        if self.world.getBlockAt(x, y, z).isPassable:
            self.x, self.y, self.z = self.world.adjustPos(x, y, z)
            return True
        return False
        #print("Can't move there!")

    def interact(self, cardinal):
        '''Returns true if the interaction was completed (Block destroyed, moved there, interactet etc.), false otherwise.'''
        x, y, z = self.cardinalToXYZ(cardinal)
        if not self.world.getBlockAt(x, y, z).isPassable():
            #Add Attack strength!
            loot = self.world.attackBlockAt(x, y, z)
            if loot is not None:
                self.inventory.addItem(*loot)
        else:
            return self.move(cardinal)
        return False
        
    def setTarget(self, x, y, z):
        self.targets = []
        self.appendTarget(x, y, z)
        
    def appendTarget(self, x, y, z):
        self.targets.append((x, y, z))
        
    def act(self):
        #This actually can't attack at a distance right now!
        if (self.x, self.y, self.z) == self.currentTarget:
            self.currentTarget = None
            
        if len(self.targets) > 0 and self.currentTarget == None:
            target = self.targets.pop(0)
            self.path = self.getPath(self.x, self.y, self.z, target[0], target[1], target[2])
            
        if len(self.path) > 0:
            if self.interact(self.path[0]):
                self.path.pop(0)
                    
    def getPath(self, fromX, fromY, fromZ, toX, toY, toZ, untilAdjecent = False):
        '''The A* pathfinding algorithm. Returns the shortest path between the given points as a list of cardinals to follow that can NOT cross the edges of the map. Assumes that not crossing Blocks is always better than doing it.'''
            
        cardinalList = CardinalDirections.__members__.values()
        origin = self.world.adjustPos(fromX, fromY, fromZ)
        goal = self.world.adjustPos(toX, toY, toZ)
        
        def getNeighbours(node):
            neighbours = [(node[0] + card.x, node[1] + card.y, node[2] + card.z) for card in cardinalList]
            if untilAdjecent:
                if goal in neighbours:
                    return reconstructPath(node)
            neighbours = list(filter(lambda x: self.world.coordinateValid(*x), neighbours))
            return neighbours
            
        def reconstructPath(node):
            #Reconstructing the path
            totalPath = []
            while node in lastStep.keys():
                old = node
                node = lastStep[node]
                diff = (old[0] - node[0], old[1] - node[1], old[2] - node[2])
                totalPath.insert(0, Vectors.getCardinalDirection(*diff))
                
            print(totalPath)
            return totalPath
            
        def appendScore(current, neigh, assumedScore):
            lastStep[neigh] = current
            directScore[neigh] = assumedScore
            detourScore[neigh] = assumedScore + Vectors.euclideanDistance(*neigh, *goal)
            
        def calcNeigh(neigh, current):
            if neigh in tested:
                return
                
            if neigh not in toTest:
                toTest.add(neigh)
                
            assumedScore = directScore[current] + 1 + self.world.getBlockAt(*neigh).health * self.world.size * self.world.size
            if assumedScore >= directScore[neigh]:
                return
            
            appendScore(current, neigh, assumedScore)
        
        #All nodes tested so far
        tested = set()
        #All nodes that need to be tested
        toTest = set()
        toTest.add(origin)
        #Maps nodes to the nodes that lie before them in the shortest path to them
        lastStep = {}
        
        #Maps from all nodes to the cost from (fromX, fromY, fromZ) to that node.
        directScore = {(a,b,c): math.inf for a, b, c in itertools.product(range(self.world.size), range(self.world.size), range(self.world.height))}
        #Getting to the start is obviously free
        directScore[origin] = 0
        #Maps from all nodes to the cost from (fromX, fromY, fromZ) to the goal using the node
        detourScore = directScore.copy()
        #We assume that we just can take the shortest way from the start
        detourScore[origin] = Vectors.stepDistance(*origin, *goal)
        
        while len(toTest) > 0:
            current = min(toTest, key=lambda x: detourScore[x])
            toTest.remove(current)
            
            if current == goal:
                return reconstructPath(current)
                
            tested.add(current)
        
            neighbours = getNeighbours(current)
            for neigh in neighbours:
                calcNeigh(neigh, current)
                
        return [CardinalDirections.INVALID]
            
                
