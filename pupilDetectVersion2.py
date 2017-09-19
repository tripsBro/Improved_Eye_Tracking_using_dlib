import cv2
import numpy as np
import imutils as im
import dlib
from skimage import io

cap = cv2.VideoCapture('/home/rahul/Videos/new/aryan-6-10-2017_1200.h264')

detector = dlib.simple_object_detector("/home/rahul/Documents/github/VR Perimetri/RequiredFiles/detector.svm")
Goteye = dlib.simple_object_detector("/home/rahul/Documents/github/VR Perimetri/RequiredFiles/GotEye.svm")
eyeDetected = False
buffer = 0
while True:
    ret, frame = cap.read()
    frame = im.resize(frame,640,480,cv2.INTER_AREA)
    output = frame.copy()
    rects = Goteye(frame)



    if len(rects)>0 and eyeDetected==False :
        buffer += 1

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, 'Hold on, stabilizing it!', (0, 30), font, 1, (200, 255, 155), 2, cv2.LINE_AA)

        if buffer==20:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, 'Got it! continue', (0, 50), font, 1, (200, 255, 155), 2, cv2.LINE_AA)

            eyeDetected = True

        for k, d in enumerate(rects):


            cv2.rectangle(output,(d.left(),d.top()),(d.right(),d.bottom()),(0,255,255))

    if eyeDetected:
        cv2.destroyWindow("waiting to confirm...")
        dets = detector(frame)

        for k, d in enumerate(dets):


            cv2.rectangle(output,(d.left(),d.top()),(d.right(),d.bottom()),(0,0,255))
            x = int((d.left() +d.right())/2)
            y = int((d.top()+d.bottom())/2)
            print "coordinates of eye:",(x,y)
            cv2.circle(output,(x,y),2,(0,255,255),2)
            pupil = frame[d.top():d.bottom(), d.left():d.right()]

        if len(dets)==0:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(output, 'Please hold on a little longer...', (0, 50), font, 1, (200, 100, 155), 2, cv2.LINE_AA)


        # cv2.imshow("out",edge)
        cv2.imshow("mid",output)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    else:

        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, 'Please wait, waiting to confirm...', (0, 130), font, 1, (200, 255, 155), 2, cv2.LINE_AA)
        cv2.imshow("waiting to confirm...", frame)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break


cap.release()
cv2.destroyAllWindows()



