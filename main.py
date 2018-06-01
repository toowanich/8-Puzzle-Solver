#Notation:
#   | 1 | 2 | 3 |
#   | 4 | 5 | 6 |
#   | 7 | 8 | 9 |
# U - Up | D - Down - | L - Left | R - Right
import math
from multiprocessing import Process, Queue
from anytree import *

finished = "123456780" #for reference
def totalWeight(x): #Finds the total weight (using manhattan distance)
    weight = 0;
    for i in range(3):
        for j in range(3):
            temp = x[(i*3)+j:(i*3)+j+1] #Gets the required string part
            if(temp != "" and temp!="0"):
                ori = originalPos(int(temp),3)
                weight += abs(ori[0]-i)+abs(ori[1]-j)
                #print(str(ori) +" " +str(temp))
    return weight
def originalPos(x,d): #takes in a number, and the width of grid
    x -=1
    a = math.floor(x/d)
    b = x%d
    return (a,b)

def currentPos(x,state):
    x = str(x)
    pos =0
    for i in range(len(state)):
        if(x==state[i]):
            pos = i
            break
    return(math.floor(pos/3),pos%3)
def stringPos(currentPos):
    return currentPos[0]*3+currentPos[1]
def isValid(state):
    inv = 0
    length = len(state)
    check = math.sqrt(length)
    if(check.is_integer() and state!=""):
        for i in range(length):
            for j in range(i+1,length):
                a = int(state[i])
                b = int(state[j])
                # print((a,b))
                if(a==0 or b==0):
                    continue
                elif(a>b):
                    inv+=1
    else:
        return False
    if(inv %2 == 1):
        return False
    else:
        return True
def findNearbyNode(zpos):
    nearbyNode=[]
    pos = [(1,0),(-1,0),(0,1),(0,-1)]

    for i,j in pos:
        nbNode = (zpos[0]+i,zpos[1]+j)
        if(not(nbNode[0]>2 or nbNode[0]<0 or nbNode[1]>2 or nbNode[1]<0)):
            nearbyNode.append(nbNode)
    nearbyString=[]
    for i in range(len(nearbyNode)):
        nearbyString.append(stringPos(nearbyNode[i]))
    return nearbyString

def createStates(currentState, visited):
    zpos = currentPos(0,currentState)
    zpos = int(stringPos(zpos))
    nearbyString=findNearbyNode(zpos)
    nextStates=[]
    for s in nearbyString:
        temp = int(currentState[s])
        if(zpos < temp):
            a = zpos
            b = s
        else:
            b = zpos
            a = s
        #print(currentState[:a],currentState[b],currentState[a+1:b],currentState[a],currentState[b+1:])
        temp = currentState[:a]+currentState[b]+currentState[a+1:b]+currentState[a]+currentState[b+1:]
        if(temp not in visited):
            print(temp)
            nextStates.append(temp)
            visited.add(temp)
    return nextStates

def process(state,queue,i):
    weight = totalWeight(state)
    queue.put(AnyNode(state = state, weight = weight))
    #print(nodes)
    #print(RenderTree(parent))
def populate(nextStates,parentNode, q,n,l):
    p = []
    for i in range(len(nextStates)):
        p.append(Process(target=process, args=(nextStates[i],queue,i,)))
        p[i].start()
    for i in range(len(nextStates)):
        p[i].join()
    for i in range(1,q.qsize()):
        temp = q.get()
        temp.parent = n[parentNode]
        n.append(temp)
        l.append(len(n)-1)
def minLeaf(l,n):
    min = 999
    for leaf in l:
        if(n[leaf].weight < min):
            min = n[leaf].weight
            node = leaf
    return node

if __name__=='__main__':
    #q = input('Enter ?')
    queue = Queue()
    q = "123405678"
    nodes = []
    leaves = []
    visited = set()
    visited.add(q)
    currentState = q
    leaves.append(0)
    nodes.append(AnyNode(state = q, weight = totalWeight(q)))
    print("Starting State: "+q)

    if(isValid(q)):
        for i in range(20):
            current = len(nodes)-1
            parentNode = minLeaf(leaves,nodes)
            if(nodes[parentNode].state == finished):
                break
            nextStates = createStates(nodes[parentNode].state, visited)
            populate(nextStates,parentNode,queue,nodes,leaves)
            leaves.remove(parentNode)
            current =len(nodes)-1
        print(RenderTree(nodes[0]))
    else:
        print("Not Valid")
