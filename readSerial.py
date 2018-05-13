import serial
ser=serial.Serial(port='COM10',baudrate=9600, timeout=0.5)

def readSerial()
    return ser.read(100) #reading up to 100 bytes
        