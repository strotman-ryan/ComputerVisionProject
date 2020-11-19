
from picamera import PiCamera
from time import sleep
import cv2 
import numpy as np

camera = PiCamera()


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
cv2.cv2.waitKey(0)  