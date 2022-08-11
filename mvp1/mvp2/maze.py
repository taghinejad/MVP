from collections import deque
import json



def checkVisited(lst,cur):
    for x in lst:
        if x[0]==cur[0] and x[1]==cur[1]:return True
    return False
        
def solveMaze(maze):
    R, C = len(maze), len(maze[0])

    start = (0, 0)
    for r in range(R):
        for c in range(C):
            if maze[r][c] == 'S':
                start = (r, c)
                break
        else: continue
        break
    else:
        return None

    queue = deque()
    final= deque()
    #zero below means the distance from starting point
    queue.appendleft((start[0], start[1], 0,[(start[0], start[1])]))
    #direction that we can go.
    directions = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    visited = [[False] * C for _ in range(R)]

    while len(queue) != 0:
        coord = queue.pop()
        visited[coord[0]][coord[1]] = True

        if maze[coord[0]][coord[1]] == "E":
            #return distance which is stored in coord[2]
            dis=coord[2]
            path=coord[3]
            final.appendleft((dis,path))
            continue
            # return dis,path insert continue

        #go the every direction and save the directions.
        for dir in directions:
            nr, nc = coord[0]+dir[0], coord[1]+dir[1]

            exist=checkVisited(coord[3],(nr,nc,1))
            if (nr < 0 or nr >= R or nc < 0 or nc >= C or maze[nr][nc] == "#" or exist): 
                continue
            # print("checking r:"+str(nr)+ " c: "+str(nc)+ "    -d:"+str(coord[2]+1))
            #append to end of the queue
            parent=coord[3].copy()
            current=(nr,nc)
            parent.append(current)
            queue.appendleft((nr, nc, coord[2]+1,parent))
    return final

def readfromfile(fname):
    with open(fname) as f:
        maze=[]
        for line in f:
            maze.append([i for i in line.strip("\n")])
    return maze



def mapMaze(n):
    colname={'A':1,'B':2, 'C':3, 'D':4 , 'E':5 , 'F':6 , 'G':7 , 'H':8 , 'I':9 , 'J':10 , 'K':11 , 'L':12 , 'M':13 , 'N':14 , 'O':15 ,
 'P':16 , 'Q':17 , 'R':18 , 'S':19 , 'T':20 , 'U':21 , 'V':22 , 'W':23 , 'X':24 , 'Y':25 ,'Z':26 }
    namecol={1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I',10:'G',11:'K',12:'L',13:'5',14:'N',15:'O',16:'P',17:'Q',18:'R',19:'S',20:'T',21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z'}
    x=int(n[1:])-1
    y=int(colname[n[0]])-1
    return (x,y)
def mapRMaze(n):
    namecol={1:'A',2:'B',3:'C',4:'D',5:'E',6:'F',7:'G',8:'H',9:'I',10:'G',11:'K',12:'L',13:'5',14:'N',15:'O',16:'P',17:'Q',18:'R',19:'S',20:'T',21:'U',22:'V',23:'W',24:'X',25:'Y',26:'Z'}
    x=n[0]+1
    y=n[1]+1
    z=str(namecol[y])+str(x)
    return z





def retPath(path):
    ar=[]
    for p in path:
        x=mapRMaze(p)
        print(x, end =" ")
        ar.append(x)
    return ar
def showPath(paths):
    i=1
    if  len(paths)>0:
        short=10000
        shortest=paths[0]
        long=0
        longest=paths[0]
        print("all the pathes that found are: ")
        while len(paths) != 0:
            path = paths.pop()
            if path[0]<short:
                shortest=path
                short=path[0]
            if path[0]>long:
                longest=path
                long=path[0]

            print (str(i)+")  steps: "+str(path[0])+" _path:"+ str(path[1]))
            i+=1
        print ("\n shortest path steps: "+str(shortest[0]))
        # print (shortest[1])
        shorti=retPath(shortest[1])
        print ("\n longest path steps: "+str(longest[0]))

        longi=retPath(longest[1])
        # print (longest[1])
        return shorti,longi
    else:
        print("No path is found")

def InitMaze(gridsize,walls,entrance,destination):
    ##initilizing
    gr=gridsize.split("x")
    row=int(gr[0])
    col=int(gr[1])
    mz=[]
    for i in range(row):
        q=[]
        for j in range(col):
            q.append(".")
        mz.append(q)
    
    i,j=mapMaze(entrance)
    mz[i][j]="S"


    for w in walls:
        i,j=mapMaze(w)
        mz[i][j]="#"
    if destination is None:
        for c in range (col):
            if mz[row-1][c]==".":
                mz[row-1][c]="E"
    else:
        i,j=mapMaze(destination)
        mz[i][j]="E"
    return mz

def resolveMaze(gridsize,walls,entrance,distination):
    wallss=walls.split(",")
    mz=InitMaze(gridsize,wallss,entrance,distination)
    paths=solveMaze(mz)
    shortest,longest=showPath(paths)
    return shortest,longest

