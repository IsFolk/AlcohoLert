from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import os
import shutil
import glob
import multiprocessing
from multiprocessing import Process, Queue
import AirAlcoholSensor
import upload_carstatus as carstatus

total = 0

Q = Queue()
def job():
    ##print(AirAlcoholSensor.detect())
    Q.put(AirAlcoholSensor.detect())


p = multiprocessing.Process(target=job)


def face_detect():
    # construct the argument parser and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--cascade", required=True,
        help = "path to where the face cascade resides")
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
    blow_count = 0 
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
        
        
        # if the `k` key was pressed, write the *original* frame to disk
        if len(rects)!=0:
            start = time.time()
            #print("Face Detected")            
            #carstat = 2
            carstat = carstatus.getStatus()
            ##print(type(carstat))
            
            if carstat != 3:
            
                p = multiprocessing.Process(target=job)
                
                p.start()
                
                temp = Q.get()
                ##print("Here is temp:",temp)
                
                if temp["Status"] == 1:
                    carstatus.uploadCarStatus(1)
                    if blow_count == 0:                
                        blow_start = temp["Time"]
                    else:
                        blow_end = temp["Time"]
                    if blow_count > 0:
                        #print(blow_end - blow_start)
                        if blow_end - blow_start > 10:
                            #print("upload")
                            carstatus.uploadCarStatus(2)
                    blow_count += 1
                elif temp["Status"] == 2:
                    carstatus.uploadCarStatus(2)
                    
                p.join()
            
        elif len(rects) == 0:
            end_collect = time.time()
            if end_collect - start_collect > 10:
                print("Face Not Detected")
            else:
                ##print(end - start)
                pass


face_detect()




cv2.destroyAllWindows()
vs.stop()



