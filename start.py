from settings import *
from transcribe_streaming_mic import processCurrentRequest
from synthesize_text import synthesize_text
from nextMoveCalculator import *
import re
import time

actionArray = []
flag = 0
exitReached = 0
destinationReached = 0
exitRequest = 0
destinationRequest = 0
exitApplication = 0

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

    while grid:
        grid.pop()
    
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
    global exitApplication
    while(1):
        global destinationReached
        global exitReached
        global destinationRequest
        global exitRequest
        command = processCurrentRequest()


        if re.search(r'\b(hello|honey)\b', command, re.I):
            synthesize_text("Welcome home, honey. How should I guide you today")
            return

        if re.search(r'\b(help|take|table)\b', command, re.I):
            if (destinationReached == 0):
                destinationRequest = 1
                synthesize_text("Calculating route.")
                routePathing()
                return


        if re.search(r'\b(return|back|entrance|out)\b', command, re.I):
            if (exitReached == 0):
                exitRequest = 1
                setSTARTPOS(getENDPOS())
                setENDPOS((0,0))
                gridGenerator()
                synthesize_text("Calculating route back.")
                routePathing()
                return

        if re.search(r'\b(face|front|desk|cupboard)\b', command, re.I):
            if (destinationReached == 1):
                itemDetection()
                synthesize_text("Do you need anything else?")
                return

        if re.search(r'\b(exit|quit)\b', command, re.I):
            synthesize_text('Goodbye Honey..')
            exitApplication = 1
            return

def routePathing():
    global destinationReached
    global destinationRequest
    global exitReached
    global exitRequest

    if destinationRequest == 1:
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
                destinationRequest = 0
                synthesize_text("You have reached your destination. Do you have any other requests?")
    
    if exitRequest == 1:
        while(exitReached == 0):
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
                exitReached = 1
                exitRequest = 0
                synthesize_text("You have reached the exit. Have a nice day!")
    

def updateStateMatrix():
    global actionArray
    serial = None
    #time.sleep(2)
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
    

def itemDetection():
    while (str(serial) == "None"):
        serial = readSerial()
    if (serial):
        serial = str(serial)
        serialList = serial.split("\n")
        for item in serialList
            item = item.replace("b","").replace("\r","").replace("'","")
            if (str(item[1]) == "9"):
                if(str(item[0]) == "1"):
                    synthesize_text("Here you are keeping the muffins, honey!")
                    return
            elif(str(item[1]) == "A")):
                if(str(item[0]) == "1"):
                    synthesize_text("Those are your bubblegums, honey.")
                    return

initStateMatrix()
gridGenerator()
while(exitApplication == 0):
    sttCommand()
            
