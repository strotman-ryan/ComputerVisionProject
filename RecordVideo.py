
from picamera import PiCamera
from time import sleep
import cv2 
import numpy as np

resolution = (3280,2464)
camera = PiCamera(resolution = resolution)
camera.framerate = 15 #set to 15 fps

videoPath = './Video/video3.h264'
camera.start_preview()
sleep(3)
print("starting recording")
camera.start_recording(videoPath)
camera.wait_recording(7)
camera.stop_recording()
print("end of recording")

'''
def ImagedDifference(img1, img2, threshold):
    difference = img1 - img2
    difference = np.absolute(difference)
    difference = Standardize(difference)
    difference[difference > threshold] = 1
    difference[difference <= threshold] = 0
    return difference


def CaptureImage(name):
    camera.start_preview()
    sleep(2)
    camera.capture(name)
    camera.stop_preview()

def Standardize(image):
    xMin = image.min()
    xMax = image.max()
    return (image - xMin) /(xMax - xMin)


firstImagePath = './Images/first.png'
secondImagePath = './Images/second.png'
CaptureImage(firstImagePath)
CaptureImage(secondImagePath)


firstImage = cv2.imread(firstImagePath,0) * 1.0

secondImage = cv2.imread(secondImagePath,0) * 1.0

difference = firstImage - secondImage
difference = np.absolute(difference)
difference = Standardize(difference)
threshold = .3
difference[difference > threshold] = 1
difference[difference <= threshold] = 0
cv2.imshow("difference", difference)
cv2.imshow(firstImagePath,firstImage)

'''