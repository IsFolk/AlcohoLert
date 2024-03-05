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
import gps_position
import blinking
import mp3.play_blow_notif as pbn
import queue


event = multiprocessing.Event()

def gps():
    Q_gps.put(gps_position.getPositionData())
def keep_get_data():
    while True:
        time.sleep(5)
        #position = gps_position.getPositionData()
        #if position != 0 and position != None:
            #if position[0] != '0.0' and position[0] != '0':
                #carstatus.uploadPosition(position[0],position[1])
        position = [0,0]
        position[0]=25.04
        position[1]=121.189
        carstatus.uploadPosition(position[0],position[1])
        print("Here is poition:",position)
        if event.is_set():
            break
        
p_gps = multiprocessing.Process(target=keep_get_data)
p_gps.start()

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
    vs = VideoStream(usePiCamera=True).start()
    time.sleep(2.0)
    
    face_before = False
    total = 0
    blow_count = 0
    face_warn_array = []
    start = time.time()
    start_collect = time.time()


    # loop over the frames from the video stream
    while True:
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
        
        

        if len(rects)!=0:
            face_before = True
            face_warn_array = []
            blinking.open_led()
            start = time.time()
            print("Face Detected")
            print("LED")
            
            
            if total == 100:
                total = 0
                #alcohol = 0.25
        
            p = os.path.sep.join([args["output"], "{}.jpg".format(
                str(total).zfill(5))])
            cv2.imwrite(p, orig)
            total += 1
            start_collect = time.time()

            # get status and check
            carstat = carstatus.getStatus()
            
            if carstat != 3:
                temp = AirAlcoholSensor.detect()

                # blow and go to face recognition
                if temp["Status"] == 1:
                    if temp["Blowed"] == 1:
                        carstatus.uploadBlowed(1)
                        event.set()
                        return
                    else:
                        #if not blow keep status 1
                        carstatus.uploadCarStatus(1)
                        if blow_count == 0:                
                            blow_start = temp["Time"]
                        else:
                            blow_end = temp["Time"]
                        if blow_count > 0:
                            #if not blow over 30 sec
                            if blow_end - blow_start > 30:
                                #print("upload")
                                pbn.notBlow_notify()
                                carstatus.uploadCarStatus(2)
                                carstatus.uploadHighSusTime()
                                event.set()
                                return
                                
                        blow_count += 1
                elif temp["Status"] == 2:
                    carstatus.uploadCarStatus(2)
                    carstatus.uploadBlowingRecord(temp["Value"])
                    carstatus.uploadHighSusTime()
                    event.set()
                    return
                
                
        elif len(rects) == 0:
            print("Not Detect")
            blinking.close_led()
            end_collect = time.time()
            
            
            face_warn_array.append(time.time())
            time_range = face_warn_array[len(face_warn_array)-1] - face_warn_array[0]
            
            #print(time_range)
            if  time_range > 7 and face_before:
                pbn.face_warning_notify()
                face_warn_array = []
                    
            
            if end_collect - start_collect > 30:   
                for file in glob.glob("/home/pi/Desktop/project_use/face_recog/dataset/test/*"):
                    os.remove(file)
                face_before = False
                    
        
#p_airsensor = multiprocessing.Process(target=sensor)
p_face_detect = multiprocessing.Process(target=face_detect)
p_face_detect.start()
p_face_detect.join()
p_gps.join()
cv2.destroyAllWindows()



