import cv2
from blob_detection import *
import numpy as np

img = cv2.imread('samples/ogwau.jpeg') # Load in grayscale for simplicity

circleBlobParams = CircleBlobParams()

circleBlobParams.detectParams.minArea = 500
circleBlobParams.drawParams.thickness = 50
circleBlobParams.drawParams.lineType = cv2.LINE_4
circleBlobParams.drawParams.noise = (-10, 50)
circleBlobParams.drawParams.grain = (-250, 250)

circleBlobDetector = CircleBlobDetector(circleBlobParams)

keypoints = circleBlobDetector.detect(img)

# Draw detected blobs as red circles on transparent overlay
print("Drawing keypoints \n")
blobs = circleBlobDetector.drawKeypoints(img, keypoints)



#  Show the image with detected blobs
cv2.imshow("Blobs", blobs)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("DONE")