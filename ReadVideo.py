
from picamera import PiCamera
from time import sleep
import cv2 
import numpy as np

def Standardize(image):
    xMin = image.min()
    xMax = image.max()
    return (image - xMin) /(xMax - xMin)

def ImagedDifference(img1, img2, threshold):
    difference = img1 - img2
    difference = np.absolute(difference)
    difference = Standardize(difference)
    difference[difference > threshold] = 1
    difference[difference <= threshold] = 0
    return difference

video_path = "./Images/video.h264"
video_object = cv2.VideoCapture(video_path)

frames = []
ret,frame = video_object.read() 
while(ret) :
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frames.append(gray)
    ret,frame = video_object.read()  

firstFrame = frames[0]
lastFrame = frames[len(frames) -1]
difference = ImagedDifference(firstFrame, lastFrame, .7)
print(difference)
cv2.imshow("difference", difference)
cv2.imshow('1', firstFrame)
cv2.imshow('last', lastFrame)

cv2.waitKey(0)