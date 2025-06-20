from blob_detection import *
from draw_tools.draw_tools import *
from image.image import *

import cv2
import numpy as np


def displayImage(img, title="Image"):
    """
    Displays an image in a window.
    """
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# TESTING CIRCLE BLOB DETECTOR
# img = cv2.imread('samples/ogwau.jpeg') # Load in grayscale for simplicity

# circleBlobParams = CircleBlobParams()

# circleBlobParams.detectParams.minArea = 500

# drawParams = DrawParams()
# drawParams.thickness = 3
# drawParams.lineType = cv2.LINE_4
# drawParams.color = (255, 255, 255)
# drawParams.noise = (-10, 50)
# drawParams.grain = (-250, 0)  

# circleBlobDetector = CircleBlobDetector(circleBlobParams)

# keypoints = circleBlobDetector.detect(img)

# # Draw detected blobs as red circles on transparent overlay
# print("Drawing keypoints \n")
# blobs = circleBlobDetector.drawKeypoints(img, keypoints, drawParams)

#  Show the image with detected blobs
# displayImage(blobs, "Detected Blobs")

# TESTING IMAGE STACKING
img = cv2.imread('samples/ogwau.jpeg')

# Base Image:
baseImage = BaseImage('samples/ogwau.jpeg', scale=1.0)

# Basic render:
renderImage = baseImage.getRenderedImage()

displayImage(renderImage, "Base Image")

# Base Image with another stacked on top


# Resizing children

# Resizing base


# Moving children relatively

# Adding sketch





print("DONE WITH TESTS")