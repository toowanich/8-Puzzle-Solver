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
            return(i)
def stringPos(currentPos):
    return currentPos[1]*3+currentPos[0]
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
#Sequential Version
# def createStates(currentState, visited):
#     zero = currentPos(0,currentState)
#     nextStates = []
#     currentState = list(currentState)
#     pos = []
#     if(zero%3 <=1):
#         pos.append(zero+1)
#     if(zero%3 >=1):
#         pos.append(zero-1)
#     if(math.floor(zero/3) <=1):
#         pos.append(zero+3)
#     if(math.floor(zero/3) >=1):
#         pos.append(zero-3)
#     for x in pos:
#         new = currentState.copy()
#         new[zero],new[x] = new[x],new[zero]
#         check = ''.join(map(str, new))
#         if(check not in visited):
#             visited.add(check)
#             nextStates.append(check)
#     #print(nextStates)
#     return nextStates
def createStates(currentState, visited):
    p=[]
    q = Queue()
    zero = currentPos(0,currentState)
    nextStates = []
    currentState = list(currentState)
    pos = []
    if(zero%3 <=1):
        pos.append(zero+1)
    if(zero%3 >=1):
        pos.append(zero-1)
    if(math.floor(zero/3) <=1):
        pos.append(zero+3)
    if(math.floor(zero/3) >=1):
        pos.append(zero-3)
    for i in range(len(pos)):
        p.append(Process(target=generate, args=(pos[i],currentState,zero,q)))
        p[i].start()
    for i in range(len(pos)):
        p[i].join()
    while(q.empty() != True):
        check = q.get()
        if(check not in visited):
            visited.add(check)
            nextStates.append(check)
    return nextStates
    #print(nextStates)
def generate(x,currentState,zero,queue):
        new = currentState.copy()
        new[zero],new[x] = new[x],new[zero]
        check = ''.join(map(str, new))
        queue.put(check)

def process(state,queue,i):
    weight = totalWeight(state)
    queue.put(AnyNode(state = state, weight = weight))
    #print(nodes)
    #print(RenderTree(parent))
def populate(nextStates,parentNode,n,l):
    p = []
    q = Queue()
    for i in range(len(nextStates)):
        p.append(Process(target=process, args=(nextStates[i],q,i,)))
        p[i].start()
    for i in range(len(nextStates)):
        p[i].join()
    while(q.empty() != True):
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
def printStep(step):
    for i in range(0,7,3):
        print("+---"*3+"+")
        print('| '+step.state[i]+' | '+step.state[i+1]+' | '+step.state[i+2]+' |')
    print("+---"*3+"+")
if __name__=='__main__':
    #q = input('Enter ?')

    q = input("Input your puzzle state: ")
    #q = "123405678"
    nodes = []
    leaves = []
    visited = set()
    visited.add(q)
    currentState = q
    leaves.append(0)
    nodes.append(AnyNode(state = q, weight = totalWeight(q)))
    print("Starting State: ")
    printStep(nodes[0])

    if(isValid(q)):
        while(1):
            current = len(nodes)-1
            parentNode = minLeaf(leaves,nodes)
            #print(nodes[parentNode])
            if(nodes[parentNode].state == finished):
                break
            nextStates = createStates(nodes[parentNode].state, visited)
            populate(nextStates,parentNode,nodes,leaves)
            leaves.remove(parentNode)
            current =len(nodes)-1
        path = nodes[parentNode].path
        for step,n in zip(path,range(len(path))):
            print("Step",n)
            printStep(step)
        #print(RenderTree(nodes[0]))
    else:
        print("Not Valid")
