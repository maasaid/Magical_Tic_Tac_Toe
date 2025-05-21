#!/usr/bin/python
# -*- coding: utf-8 -*-
# import the necessary packages

from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import cv2
import imutils
import time
# from magical-tic-tac-toe import *
# Replace the above line with the correct module name if available, e.g.:

# The import statement is already correct:
from magical_tic_tac_toe import *

# construct the argument parse and parse the arguments
tic=0

ap = argparse.ArgumentParser()
ap.add_argument('-v', '--video',
                help='path to the (optional) video file')
ap.add_argument('-b', '--buffer', type=int, default=32,
                help='max buffer size')
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space

greenLower = (5,50,50)
greenUpper = (15,255,255)

# initialize the list of tracked points, the frame counter,
# and the coordinate deltas

pts = deque(maxlen=args['buffer'])
counter = 0
(dX, dY) = (0, 0)
direction = ''

# if a video path was not supplied, grab the reference
# to the webcam

if not args.get('video', False):
    vs = VideoStream(src=0).start()
else:

# otherwise, grab a reference to the video file

    vs = cv2.VideoCapture(args['video'])

# allow the camera or video file to warm up

time.sleep(2.0)

# keep looping
def x_pos_org(x):
    if (int(x) in range(170,270)):
        return 0
    elif (int(x) in range(280,380)):
        return 1
    elif (int(x) in range(400,500)):
        return 2
def x_pos(x):
    if (int(x) in range(140,250)):
        return 0
    elif (int(x) in range(260,380)):
        return 1
    elif (int(x) in range(390,530)):
        return 2
while True:

    # grab the current frame

    frame = vs.read()

    # handle the frame from VideoCapture or VideoStream

    frame = (frame[1] if args.get('video', False) else frame)

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video

    if frame is None:
        break

    # resize the frame, blur it, and convert it to the HSV
    # color space

    frame = imutils.resize(frame, width=600)
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # construct a mask for the color "green", then perform
    # a series of dilations and erosions to remove any small
    # blobs left in the mask

    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)

    # find contours in the mask and initialize the current
    # (x, y) center of the ball

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None

    # only proceed if at least one contour was found

    if len(cnts) > 0:

        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid

        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        print("X= "+str(int(x))+"   Y= "+str(int(y))+"  radius= "+str(int(radius)))
        # only proceed if the radius meets a minimum size
#         25
# 220,160 |  330,160 |  450,160
# 220,230 |  330,230 | 450,230
# 220,310	|  330,310 |    470,310


        selected = None
        clicked=[]
        try:
            if int(radius) in range(10, 22):
                if  (int(y) in range(90,170)) and (x_pos(x) in range(3)):
                    selected = lista[x_pos(x)]
                elif (int(y) in range(180,260)) and (x_pos(x) in range(3)):
                    selected = lista[x_pos(x)+3]
                elif (int(y) in range(270,350)) and (x_pos(x) in range(3)) :
                    selected = lista[x_pos(x)+6]
                if selected and (time.perf_counter() - tic>3):
                    print(time.perf_counter() - tic)
                    clicked.append(selected)
                    xpath = "//div[@class='"+selected+"']"
                    elem = driver.find_element(By.XPATH,xpath)
                    elem.click()
                    tic = time.perf_counter()
        except:
            continue
                
        if radius > 10:

            # draw the circle and centroid on the frame,
            # then update the list of tracked points

            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0xFF,
                       0xFF), 2)
            cv2.circle(frame, center, 5, (0, 0, 0xFF), -1)
            pts.appendleft(center)

        # loop over the set of tracked points

    for i in np.arange(1, len(pts)):

        # if either of the tracked points are None, ignore
        # them

        if pts[i - 1] is None or pts[i] is None:
            continue

        # check to see if enough points have been accumulated in
        # the buffer

        if counter >= 10 and i == 10 and pts[i - 10] is not None:

            # compute the difference between the x and y
            # coordinates and re-initialize the direction
            # text variables

            dX = pts[i - 10][0] - pts[i][0]
            dY = pts[i - 10][1] - pts[i][1]
            (dirX, dirY) = ('', '')

            # ensure there is significant movement in the
            # x-direction

            if np.abs(dX) > 20:
                dirX = ('East' if np.sign(dX) == 1 else 'West')

            # ensure there is significant movement in the
            # y-direction

            if np.abs(dY) > 20:
                dirY = ('North' if np.sign(dY) == 1 else 'South')

            # handle when both directions are non-empty

            if dirX != '' and dirY != '':
                direction = '{}-{}'.format(dirY, dirX)
            else:

            # otherwise, only one direction is non-empty

                direction = (dirX if dirX != '' else dirY)

        # otherwise, compute the thickness of the line and
        # draw the connecting lines

        thickness = int(np.sqrt(args['buffer'] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 0xFF), thickness)

    # show the movement deltas and the direction of movement on
    # the frame

    cv2.putText(
        frame,
        direction,
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (0, 0, 0xFF),
        3,
        )
    cv2.putText(
        frame,
        'dx: {}, dy: {}'.format(dX, dY),
        (10, frame.shape[0] - 10),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.35,
        (0, 0, 0xFF),
        1,
        )

    # show the frame to our screen and increment the frame counter

    cv2.imshow('Frame', frame)
    key = cv2.waitKey(1) & 0xFF
    counter += 1

    # if the 'q' key is pressed, stop the loop

    if key == ord('q'):
        break

# if we are not using a video file, stop the camera video stream

if not args.get('video', False):
    vs.stop()
else:

# otherwise, release the camera

    vs.release()

# close all windows

cv2.destroyAllWindows()
