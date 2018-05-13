from settings import *
from transcribe_streaming_mic import processCurrentRequest
from synthesize_text import synthesize_text
from nextMoveCalculator import *
import re
import time

actionArray = []
flag = 0
destinationReached = 0

import serial
ser=serial.Serial(port='COM6',baudrate=9600, timeout=0.5)

def readSerial():
    return ser.read(100) #reading up to 100 bytes

def initStateMatrix():
    global actionArray
    global flag
    while(1):
        serial = readSerial()
        if (serial):
            serial = str(serial)
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
                            if(not(action[1] == "0")):
                                if(action[0] == "1"):
                                    SurfaceState[i][j] = 2
                                if(action[0] == "0"):
                                    SurfaceState[i][j] = 0
                            else:
                                if(action[0] == "1"):
                                    SurfaceState[i][j] = 1
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
        delete = getSTARTPOS()
        SurfaceState[delete[1]][delete[0]] = 0
        updateStateMatrix()
        start = getUserPosition()
        while(start == getSTARTPOS()):
            updateStateMatrix()
            start = getUserPosition()
        setSTARTPOS(start)
        end = getENDPOS()
        if(start == end):
            destinationReached = 1
            synthesize_text("You have reached your destination.")

def updateStateMatrix():
    global actionArray
    serial = None
    time.sleep(2)
    while (str(serial) == "None"):
        serial = readSerial()
    print (type(str(serial)))
    if (serial):
        serial = str(serial)
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
    return getSTARTPOS()
    



initStateMatrix()
gridGenerator()
sttCommand()
            
