
from time import sleep
import cv2 
import numpy as np
from skimage.color import rgb2yiq
from scipy.ndimage import binary_closing

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

video_path = "./Video/video3.h264"
video_object = cv2.VideoCapture(video_path)

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
    #70 150 -> video 3
    if numFrames % 10 ==0 and numFrames >= 70 and numFrames <= 170:
        cv2.imshow("FrameRGB: " + str(numFrames), rgbFrames[-1])
        difference = ImagedDifference(yiqFrames[0], yiqFrames[-1], .05) 
        #cv2.imshow("FrameDifference: " + str(numFrames),difference)
        valid, difference = RemoveSmallComponents(difference)
        if valid:
            #cv2.imshow("One Connected Component: " + str(numFrames), difference)           
            difference = binary_closing(difference, iterations=10).astype(float)
            #cv2.imshow("After closing: " + str(numFrames), difference)
            nb_components, output, stats, centroids = cv2.connectedComponentsWithStats(difference.astype(np.uint8), connectivity=8)
            diameter = stats[1,2]
            x = centroids[1][0]
            y = centroids[1][1]
            stats = (numFrames,x,y,diameter)
            frameStats.append(stats)
        else:
            print("Frame "  +str(numFrames)  + " not valid")

    ret,frame = video_object.read()  

print(frameStats)
#.05 is best for threshold
'''
for threshold in range(4,10):
    threshold = threshold / 100
    difference = ImagedDifference(yiqFrames[0], yiqFrames[-1], threshold)
    cv2.imshow("difference"  + str(threshold), difference)
'''
cv2.waitKey(0)