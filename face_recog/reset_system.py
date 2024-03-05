import os
os.system("pkill -f recognize_video.py")

from imutils.video import VideoStream
import argparse
import imutils
import time
import cv2
import shutil
import glob
import multiprocessing
import upload_carstatus as carstatus
import subprocess

total = 0

#p2.start()
#print("here is Q1",Q1.get())
#carstatus.uploadPosition(Q1.get())
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


            
        elif len(rects) == 0:
            end = time.time()
            #if end_collect - start_collect > 10:  #real
            if end - start > 5:
                
                carstatus.uploadCarStatus(0)
                carstatus.uploadBlowed(0)
                cv2.destroyAllWindows()
                subprocess.call("./face_recog.sh", shell = True)


face_detect()







