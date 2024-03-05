import os

os.system("pkill -f reset_system.py")

from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import shutil
import glob
import multiprocessing
from multiprocessing import Process, Queue
import AirAlcoholSensor
import upload_carstatus as carstatus
#import gps_position
import gps_position
import blinking
import mp3.play_blow_notif as pbn

total = 0
#warining = 0
Q = Queue()

def job():
    ##print(AirAlcoholSensor.detect())
    Q.put(AirAlcoholSensor.detect())
    Q.put(gps_position.getPositionData())

p = multiprocessing.Process(target=job)
#p2.start()
#print("here is Q1",Q1.get())
#carstatus.uploadPosition(Q1.get())
def face_detect():
    gps_array = []
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cascade", required=True,
        help = "path to where the face cascade resides")
    ap.add_argument("-o", "--output", required=True,
        help="path to output directory")
    args = vars(ap.parse_args())



    # load OpenCV's Haar cascade for face detection from disk
    detector = cv2.CascadeClassifier(args["cascade"])
    # initialize the video stream, allow the camera sensor to warm up,
    # and initialize the total number of example faces written to disk
    # thus far
    #print("[INFO] starting video stream...")
    # vs = VideoStream(src=0).start()
    vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)
    total = 0
    #warning = 0
    blow_count = 0 
    start = time.time()
    start_collect = time.time()


    # loop over the frames from the video stream
    while True:
        #print("cv2")

        # grab the frame from the threaded video stream, clone it, (just
        # in case we want to write it to disk), and then resize the frame
        # so we can apply face detection faster
        frame = vs.read()
        orig = frame.copy()
        frame = imutils.resize(frame, width=400)
        # detect faces in the grayscale frame
        rects = detector.detectMultiScale(
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY), scaleFactor=1.1, 
            minNeighbors=5, minSize=(30, 30))
        # loop over the face detections and draw them on the frame
        for (x, y, w, h) in rects:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # show the output frame
        cv2.imshow("Frame", frame)
        
        key = cv2.waitKey(1) & 0xFF
        
        
        # if the `k` key was pressed, write the *original* frame to disk
        if len(rects)!=0:
            print("Detect")
            blinking.open_led()
            start = time.time()
            #print("Face Detected")
            print("LED")
            
            
            if total == 100:
                total = 0
                alcohol = 0.25
        
            p = os.path.sep.join([args["output"], "{}.jpg".format(
                str(total).zfill(5))])
            cv2.imwrite(p, orig)
            total += 1
            #warning += 1
            start_collect = time.time()

            
            
            #carstat = 2
            carstat = carstatus.getStatus()
            ##print(type(carstat))
            
            if carstat != 3:
            
                p = multiprocessing.Process(target=job)
            
                p.start()
                
                temp = Q.get()
                position =Q.get()
                
                print(position)
                if position != 0 and position != None:
                    if position[0] != '0.0' and position[0] != '0':
                        carstatus.uploadPosition(position[0],position[1]) #tuple's index stand for lat&lon
                        #print("uploaded position!")                    
                        print("Here is poition:",position)
                #print("positon[0]'s type",type(position[0]))
                if temp["Status"] == 1:
                 
                    if temp["Blowed"] == 1:
                        p.join()
                        carstatus.uploadBlowed(1)
                        return
                    else:
                        carstatus.uploadCarStatus(1)
                        if blow_count == 0:                
                            blow_start = temp["Time"]
                        else:
                            blow_end = temp["Time"]
                        if blow_count > 0:
                            #print(blow_end - blow_start)
                            if blow_end - blow_start > 30:
                                #print("upload")
                                #pbn.notBlow_notify()
                                carstatus.uploadCarStatus(2)
                                carstatus.uploadHighSusTime()
                                p.join()
                                return
                        blow_count += 1
                elif temp["Status"] == 2:
                    carstatus.uploadCarStatus(2)
                    carstatus.uploadBlowingRecord(temp["Value"])  ##
                    carstatus.uploadHighSusTime()
                    p.join()
                    return
                    
                p.join()
            
        elif len(rects) == 0:
            print("Not Detect")
            end_collect = time.time()
            #pbn.face_warning_notify()
            
            #if end_collect - start_collect > 10:  #real
            if end_collect - start_collect > 10:   
                for file in glob.glob("/home/pi/Desktop/project_use/face_recog/dataset/test/*"):
                    os.remove(file)
                
                position = gps_position.getPositionData()
                #print("position is:",position)
                
                if position != 0 and position != None:
                    #blinking.blink()
                    if position[0] != '0.0' and position[0] != '0':
                        gps_array.append([position[0], position[1]])
                        #print("array:",gps_array)
                    
                if len(gps_array) == 2:
                    if gps_array[0][0][3:6] != gps_array[1][0][3:6] and gps_array[0][1][4:8] != gps_array[1][1][4:8]:
                        carstatus.uploadCarStatus(2)
                        carstatus.uploadHighSusTime()
                        
                        return

                    gps_array = []
                        
                    
            
            
            else:
                ##print(end - start)
                pass


face_detect()


cv2.destroyAllWindows()



