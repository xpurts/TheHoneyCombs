import collections
from synthesize_text import synthesize_text
from settings import grid

obstacle, clear, goal = "#", ".", "*"
width, height = 3, 3

STARTPOS = (0,0)
ENDPOS = (2,2)

def bfs(grid, start):
    queue = collections.deque([[start]])
    seen = set([start])
    while queue:
        path = queue.popleft()
        x, y = path[-1]
        if grid[y][x] == goal:
            return path
        for x2, y2 in ((x+1,y), (x-1,y), (x,y+1), (x,y-1)):
            if 0 <= x2 < width and 0 <= y2 < height and grid[y2][x2] != obstacle and (x2, y2) not in seen:
                queue.append(path + [(x2, y2)])
                seen.add((x2, y2))

def setDirection(currentPosition, nextPosition):
    xDirection = currentPosition[1] - nextPosition[1]
    yDirection = currentPosition[0] - nextPosition[0]

    if(yDirection > 0 and xDirection == 0 ):
        synthesize_text("take a step to the right")
        return nextPosition
    if(yDirection < 0 and xDirection == 0 ):
        synthesize_text("take a step to the left")
        return nextPosition
    if(yDirection == 0 and xDirection > 0 ):
        synthesize_text("take a step back")
        return nextPosition
    if(yDirection == 0 and xDirection < 0 ):
        synthesize_text("take a step forward")
        return nextPosition

    synthesize_text("Error processing direction")

def directions():
    global grid
    global STARTPOS
    global ENDPOS
    print(STARTPOS)
    path = bfs(grid, STARTPOS)
    if(path == None):
        synthesize_text("NO way to reach the destination!")
        STARTPOS = ENDPOS
    else:
        print(path)
        setDirection(path[0], path[1])

def getENDPOS():
    return ENDPOS

def getSTARTPOS():
    return STARTPOS

def setSTARTPOS(start):
    global STARTPOS
    STARTPOS = start

def setENDPOS(end):
    global ENDPOS
    ENDPOS = end

# while(not(STARTPOS == ENDPOS)):
    # directions()

#path = bfs(grid, (2, 0))
# [(5, 2), (4, 2), (4, 3), (4, 4), (5, 4), (6, 4)]
# print(path)