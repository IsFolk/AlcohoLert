import serial
import time
import string
import pynmea2

def getPositionData():
    port="/dev/serial0"
    ser=serial.Serial(port, baudrate=9600, timeout=0.5)
    dataout = pynmea2.NMEAStreamReader()

    newdata=ser.readline()
    #print(newdata)
    
    if newdata[0:6] == bytes(b'$GPRMC'):
        newmsg=pynmea2.parse(newdata.decode("utf-8"))
        lat=newmsg.latitude
        lng=newmsg.longitude
        gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
        #print(gps)
    
        return str(lat),str(lng)


#l1,l2 = getPositionData()
#print(l1,l2)
#while True:
#    getPositionData()

    


