import cv2
from blob_detection import *
from draw_tools.draw_tools import *
import numpy as np

img = cv2.imread('samples/ogwau.jpeg') # Load in grayscale for simplicity

circleBlobParams = CircleBlobParams()

circleBlobParams.detectParams.minArea = 500

drawParams = DrawParams()
drawParams.thickness = 10
drawParams.lineType = cv2.LINE_4
drawParams.color = (0, 0, 0)
drawParams.noise = (-10, 50)
drawParams.grain = (-250, 0)  

circleBlobDetector = CircleBlobDetector(circleBlobParams)

keypoints = circleBlobDetector.detect(img)

# Draw detected blobs as red circles on transparent overlay
print("Drawing keypoints \n")
blobs = circleBlobDetector.drawKeypoints(img, keypoints, drawParams)



#  Show the image with detected blobs
cv2.imshow("Blobs", blobs)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("DONE")