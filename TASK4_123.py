#Work Cited:
#OpenCV: Image Thresholding, https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html
#OpenCV: Changing Colorspaces, https://docs.opencv.org/4.x/df/d9d/tutorial_py_colorspaces.html
#OpenCV: Contour Features, https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html

#Futher Imporvement:
#This code tracks objects with yellow color very well including the color coming out from the 
#phone; however, when it encounters yellow object that reflects the light, it will have 
#a lot of noises. Therefore, one of the imporvement of this code is to imporve the
#tracking ability when it encounts reflective objects.

import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)
while(1):
    # Take each frame
    _, frame = cap.read()
    # Convert BGR to HSV
    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    # define range of yellow color in HSV
    lower_yellow = np.array([20,100,100])
    upper_yellow = np.array([30,255,255])
    # Threshold the HSV image to get only yellow colors
    mask = cv.inRange(hsv, lower_yellow, upper_yellow)

    # Noise Reduction
    blur = cv.GaussianBlur(mask,(5,5),0)
    ret3,th3 = cv.threshold(blur,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

   # Bitwise-AND mask and original image
    res = cv.bitwise_and(frame,frame, mask= th3)

    contours,hierarchy = cv.findContours(th3, 1, 2)

    #creating bounding boxes
    if(len(contours) != 0):
        for cnt in contours:
           x,y,w,h = cv.boundingRect(cnt)
           cv.rectangle(res,(x,y),(x+w,y+h),(0,255,0),2)

    cv.imshow('frame',frame)
    cv.imshow('mask',th3)
    cv.imshow('res',res)
    

    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break 
    
cv.destroyAllWindows()