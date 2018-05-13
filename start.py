from settings import *
from transcribe_streaming_mic import processCurrentRequest
from synthesize_text import synthesize_text
from nextMoveCalculator import *
import re
import time
#from readSerial import readSerial

actionArray = []
flag = 0
destinationReached = 0

def initStateMatrix():
    global actionArray
    global flag
    while(1):
        serial = "b'15\r\n11\r\n'"
        serialList = serial.split("\n")
        for action in serialList:
            action = action.replace("b","").replace("\r","").replace("'","")
            if(not(action == "")):
                actionArray.append(action)
        # print(actionArray)
        
        for i in range(width):
            for j in range(height):
                for action in actionArray:
                    #print(str(SurfaceMapping[i][j]) + " " + action[1])
                    if(str(SurfaceMapping[i][j]) == action[1]):
                        if(not(action[1] == "1")):
                            if(action[0] == "1"):
                                SurfaceState[i][j] = 2
                            if(action[0] == "0"):
                                SurfaceState[i][j] = 0
                        else:
                            if(action[0] == "1"):
                                flag = 1
        
        print(SurfaceState)

        while(actionArray):
            actionArray.pop()

        if (flag == 1):
            return

def gridGenerator():
    global grid
    global ENDPOS
    for i in range(width):
        line = ""
        for j in range(height):
            if(SurfaceState[i][j] == 2):
                line+="#"
            else:
                end = getENDPOS()
                if(j == end[0] and i == end[1]):
                    line+="*"
                else:
                    line+="."
        grid.append(line)


def sttCommand():
    while(1):
        command = processCurrentRequest()
        if re.search(r'\b(help|take|table)\b', command, re.I):
            synthesize_text("Calculating route.")
            routePathing()
            return

        if re.search(r'\b(exit|quit)\b', command, re.I):
            print('Exiting..')
            return

def routePathing():
    global destinationReached

    while(destinationReached == 0):
        directions()
        updateStateMatrix()
        start = getUserPosition()
        setSTARTPOS(start)
        end = getENDPOS()
        if(start == end):
            destinationReached = 1
            synthesize_text("You have reached your destination.")

def updateStateMatrix():
    global actionArray
    time.sleep(2)
    serial = "b'01\r\n12\r\n'"
    serialList = serial.split("\n")
    for action in serialList:
        action = action.replace("b","").replace("\r","").replace("'","")
        if(not(action == "")):
            actionArray.append(action)
    # print(actionArray)
    
    for i in range(width):
        for j in range(height):
            for action in actionArray:
                if(str(SurfaceMapping[i][j]) == action[1]):
                    if(action[0] == "1"):
                        SurfaceState[i][j] = 1
                    if(action[0] == "0"):
                        SurfaceState[i][j] = 0
    
    print(SurfaceState)

    while(actionArray):
        actionArray.pop()

def getUserPosition():
    for i in range(width):
        for j in range(height):
            if(SurfaceState[i][j] == 1):
                return (j,i)



initStateMatrix()
gridGenerator()
sttCommand()
            
