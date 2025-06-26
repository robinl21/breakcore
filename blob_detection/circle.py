from .blob import BlobParams, BlobDetector

import cv2
import numpy as np
from draw_tools.draw_tools import *

import math

class CircleBlobParams(BlobParams):
    def __init__(self, minThreshold=100, maxThreshold=220, thresholdStep=10,
                 filterByColor=False, blobColor=0,
                 filterByArea=True, minArea=250, maxArea=10000,
                 filterByCircularity=False, minCircularity=0.1, maxCircularity=0.8,
                 filterByInertia=False, minInertiaRatio=0.1, maxInertiaRatio=0.6,
                 filterByConvexity=False, minConvexity=0.87, maxConvexity=0.95,
                 keypointsKept=1.0):
        super().__init__(minThreshold, maxThreshold, thresholdStep,
                         filterByColor, blobColor,
                         filterByArea, minArea, maxArea,
                         filterByCircularity, minCircularity, maxCircularity,
                         filterByInertia, minInertiaRatio, maxInertiaRatio,
                         filterByConvexity, minConvexity, maxConvexity,
                         keypointsKept)

class CircleBlobDetector(BlobDetector):
    def __init__(self, params: CircleBlobParams):
        # Creates detector and detectParams and keypoitns
        super().__init__(params)
    
    def detect(self, img):
        # Detect blobs in the image
        keypoints = self.detector.detect(img)
        indices = math.ceil(len(keypoints) * self.keypointsKept)

        # Randomly sample without replacement
        if indices > 0:
            selected_indices = np.random.choice(len(keypoints), size=indices, replace=False)
            sampled_keypoints = [keypoints[i] for i in selected_indices]
        else:
            sampled_keypoints = []

        return sampled_keypoints
    
    # TODO: parallelize this via merge sort method
    # Returns render, and mask
    def getSketchTemplate(self, img_to_draw_on, keypoints, drawParams):
        h, w = img_to_draw_on.shape[:2]
        
        overlay = img_to_draw_on.copy()

        # black background for mask
        line_mask = np.zeros((h, w, 3), dtype=np.uint8)

        # draw tracking
        for kp in keypoints:
            
            x, y = int(kp.pt[0]), int(kp.pt[1])
            radius = int(kp.size / 2)

            # drawing circles uses random noise, but we seed it to maintain consistency among mask and actual drawing
            seed = np.random.randint(0, 2**32 - 1)

            # Draw keypoint on grain mask using white
            draw_circle(line_mask, (x,y), radius, drawParams, seed, no_outline=False)


            # Draw keypoint on overlay using color
            draw_circle(overlay, (x, y), radius, drawParams, seed)

        # TODO: draw tracking lines onto line_mask and overlay

        # drawing circles uses random noise, but we seed it to maintain consistency among mask and actual drawing
        seed = np.random.randint(0, 2**32 - 1)
        draw_tracking(line_mask, keypoints, drawParams, seed, no_outline=False)
        draw_tracking(overlay, keypoints, drawParams, seed)

        return overlay, line_mask
    

    