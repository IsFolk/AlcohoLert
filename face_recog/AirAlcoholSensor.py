# MQ3 SENSOR CODE

""" 
If you have not installed the Wiring Pi Library,
install it using below command : 

sudo pip install wiringpi

"""

#Copy and Paste the below code and save it as a ".py" file

import wiringpi as wiringpi
#import pygame
import mp3.play_blow_notif as pbn
import BreathAlcoholSensor
import time
# import required modules
from pydub import AudioSegment
from pydub.playback import play
import time

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(23, 0)


def detect(): #
    
    #while True:
    my_input=wiringpi.digitalRead(23)  #1=>no alcohol 0=>have alcohol
    alcohol = {"Status": 0, "Time": time.time(), "Blowed": 0}
    
    if(my_input):
        alcohol["Status"] = 0
        print("Alcohol Not Detected !")
    else:
        alcohol["Status"] = 1
        print("Alcohol Detected")
        
        ## you can choose your own file
        # for playing wav file
        
        pbn.blow_notify()
        voltage = BreathAlcoholSensor.get_concentration()
        alcohol_concentration = (voltage -1.3)/2.778
        #print("Alcohol Concentration is:", alcohol_concentration)
        #alcohol_concentration = 0.1
        
        if voltage > 0.2:
            alcohol["Blowed"] = 1
            pbn.recog_notify()
            
        if alcohol_concentration < 0:
            alcohol["Time"] = time.time()
        
        
        if alcohol_concentration > 0.25:
            print("Alcohol Concentration is:", alcohol_concentration)
            pbn.over_notify()
            alcohol["Value"] = alcohol_concentration  ##
            alcohol["Status"] = 2
        
            
    return alcohol

#print(detect())
