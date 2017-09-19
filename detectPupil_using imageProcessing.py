import cv2
import numpy as np
import imutils as im


cap = cv2.VideoCapture('/home/rahul/Videos/new/aman-6-10-2017_1200.h264')

count = 2
while True:
    count +=1
    ret, frame = cap.read()
    frame = im.resize(frame,640,480,cv2.INTER_AREA)
    output = frame.copy()
    gray  = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # blur = cv2.bilateralFilter(gray, 3, 115, 115)
    gray = cv2.GaussianBlur(gray,(9,9),7,sigmaY=0)
    _,thresh = cv2.threshold(gray,72,255,cv2.THRESH_TRUNC)
    erode = cv2.erode(thresh, (3, 3), iterations=3, borderType=2, borderValue=cv2.MORPH_DILATE)
    adThresh = cv2.adaptiveThreshold(erode,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,111,3)
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(adThresh, cv2.MORPH_ELLIPSE, kernel, iterations=2)

    opening = cv2.erode(opening, (3, 3), iterations=2)


    edges = cv2.Canny(opening, 250,250, apertureSize=5, L2gradient=True,edges=cv2.SUBDIV2D_PTLOC_ON_EDGE)


#  ##-=====================hough circle method==========================================
#     circles = cv2.HoughCircles(edges,cv2.HOUGH_GRADIENT,8,1200,minRadius=20,maxRadius=50)
#     if circles is not None:
#         print "got a circle!"
#         # convert the (x, y) coordinates and radius of the circles to integers
#         circles = np.round(circles[0, :]).astype("int")
#
#         # loop over the (x, y) coordinates and radius of the circles
#         for (x, y, r) in circles:
#             # draw the circle in the output image, then draw a rectangle
#             # corresponding to the center of the circle
#             cv2.circle(output, (x,y), r, (0, 255, 0), 4)
#             cv2.circle(output, (x,y), 1, (255, 0, 0), -1)
#
# ##---------------------------------------------------------------------------------
            ##-=====================contour method=================================
    cnts = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        # print "c: ", c, "sh: ", c.shape
        # cv2.drawContours(output,c,-1,(255,0,0))
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
        area = cv2.contourArea(c)
        # print("area", area)
        # as1 = cv2.convexHull(c)
        # cv2.drawContours(output,c,-1,(0,0255,0),2)




        if radius > 12 and radius<40:

            cv2.circle(output, (int(x), int(y)), 1,
                     (255, 0, 255), 2)
            cv2.circle(output, (int(x), int(y)), int(radius), (0, 255, 255), 1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(output, str(radius), (0, 130), font, 1, (200, 255, 155), 2, cv2.LINE_AA)
        else:
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(output, "eye not detected", (0, 130), font, 1, (200, 255, 155), 2, cv2.LINE_AA)


            # ##----------------------------------------------------------------------------
    if count%2==0:
        cv2.imshow("input", frame)
        cv2.imshow("edge", edges)
        cv2.imshow("output", output)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()



