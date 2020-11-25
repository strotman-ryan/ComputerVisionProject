
from time import sleep
import cv2 
import numpy as np
from skimage.color import rgb2yiq
from scipy.ndimage import binary_closing
import math
import matplotlib.pyplot as plt

def Standardize(image):
    xMin = image.min()
    xMax = image.max()
    return (image - xMin) /(xMax - xMin)

#return true if ball in image
#return false if no ball
def RemoveSmallComponents(image):
    nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(difference.astype(np.uint8), connectivity=8)
    if nb_components < 2:
        return False, None
    index = np.argsort(stats[:,4])[-2] #take the second largest, the first is the background
    if stats[:,4][index] < 30:
        #area needs to be greater than 30 pixels
        return False, None
    img2 = np.zeros((output.shape))
    for i in range(0, nb_components):
        if i == index:
            img2[output == i] = 1
    return True, img2

#YIQ image
#range of I and Q coordinates are -.59 to .59
def ImagedDifference(img1, img2, threshold):
    difference = img1 - img2
    difference = np.square(difference)
    difference = difference[:,:,1] + difference[:,:,2]
    difference = np.sqrt(difference)
    difference[difference > threshold] = 1
    difference[difference <= threshold] = 0
    return difference

#theta is angle from straing up Z axis
#rho is angle from x axis; 90 at y axis
def PolarToCartesian(r,theta,rho):
    thetaRad = math.radians(theta)
    rhoRad = math.radians(rho)
    x = r * math.sin(thetaRad) * math.cos(rhoRad)
    y = r * math.sin(thetaRad)  * math.sin(rhoRad)
    z = r * math.cos(thetaRad)
    return x,y,z

#convert (x,y,diameter), to (x,y,z), (0,0,0) is camera
def convertFromDiameterToCartesion(x,y,diameter):
    #constants
    din = 2.75 #diameter of ball in inches
    w = 1280 #width of images in pixels   #TODO
    h = 720 #heigh of images in pixels   #TODO
    xFov = 62.3 #horizontal field of view in degrees
    yFov = 48.8 #Vertical field of view in degrees

    circumference = w / diameter * din   #circumfrence in inches of horizontal plane
    radius = circumference / (2 * math.pi) * 360 / xFov #distance from camera
    rho = 90 + xFov/2 - x/w * xFov #angle from x axis ball is at
    theta = 90 - yFov/2 + y/h * yFov #angle from z axis (pointing straing up)
    xFinal,yFinal,zFinal = PolarToCartesian(radius,theta,rho)
    return xFinal, yFinal, zFinal

def Magnitude(x,y,z):
    return math.sqrt(x * x + y * y + z * z)

#points are (x,y,z)
def Distance(firstPoint, secondPoint):
    return Magnitude(firstPoint[0] - secondPoint[0], firstPoint[1] - secondPoint[1], firstPoint[2] - secondPoint[2])

'''
#test convertFromDiameterToCartesion function
x = 100
y = 50
diameter = 3
print(convertFromDiameterToCartesion(x,y,diameter))
'''
'''
#test PolarToCartesan function
r = 1
theta = 100
rho = 170
print(PolarToCartesian(r,theta,rho))
'''
frameRate = 15 #frames per second
timeBetweenFrames = 60 / frameRate #in seconds
video_path = "./Video/video4.h264"
video_object = cv2.VideoCapture(video_path)

plt.scatter([1,2,4],[1,2,3])
print("iddle")
plt.show()

yiqFrames = []
rgbFrames = []
frameStats = []
ret,frame = video_object.read() 
numFrames = 0
while(ret) :
    numFrames += 1
    rgbFrames.append(frame)
    yiqFrames.append(rgb2yiq(frame))
    '''
    # Press Q on keyboard to  exit
    #this makes the video play for some reason
    if cv2.waitKey(25) & 0xFF == ord('q'): 
      break
    cv2.imshow("Frame", frame)
    '''
    #140 250 -> for video1
    #60 150 -> for video2
    #70 150 -> for video 3
    #40 70 -> for video 4
    #cv2.imshow("FrameRGB: " + str(numFrames), rgbFrames[-1])
    difference = ImagedDifference(yiqFrames[0], yiqFrames[-1], .05) 
    #cv2.imshow("FrameDifference: " + str(numFrames),difference)
    valid, difference = RemoveSmallComponents(difference)
    if valid:
        #cv2.imshow("One Connected Component: " + str(numFrames), difference)           
        difference = binary_closing(difference, iterations=10).astype(float)
        #cv2.imshow("After closing: " + str(numFrames), difference)
        nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(difference.astype(np.uint8), connectivity=8)
        diameter = stats[1,3]  #the max height of object in pixels
        x = centroids[1][0]
        y = centroids[1][1]
        stats = (numFrames,x,y,diameter)
        frameStats.append(stats)
    else:
        print("Frame "  +str(numFrames)  + " not valid")
        
        

    ret,frame = video_object.read()  


results = []
for stats in frameStats:
    results.append(convertFromDiameterToCartesion(stats[1], stats[2], stats[3]))

speedArray = []
frameArray = []
for i in range(len(results) - 1):
    distance = Distance(results[i], results[i+1])
    speed = distance / timeBetweenFrames
    speedArray.append(speed)
    frameArray.append(i)
    print(str(speed) + " inches/second")
print("ready")
plt.scatter(frameArray,speedArray)
print("iddle")
plt.show()
print("dont")
#.05 is best for threshold
#d -> 4 3/4 inches
'''
for threshold in range(4,10):
    threshold = threshold / 100
    difference = ImagedDifference(yiqFrames[0], yiqFrames[-1], threshold)
    cv2.imshow("difference"  + str(threshold), difference)
'''