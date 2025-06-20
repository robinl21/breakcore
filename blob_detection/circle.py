from .blob import BlobParams, BlobDetector

import cv2
import numpy as np
from draw_tools.draw_tools import *

class CircleBlobParams(BlobParams):
    def __init__(self, minThreshold=100, maxThreshold=220, thresholdStep=10,
                 filterByColor=False, blobColor=0,
                 filterByArea=True, minArea=250, maxArea=10000,
                 filterByCircularity=False, minCircularity=0.1, maxCircularity=0.8,
                 filterByInertia=False, minInertiaRatio=0.1, maxInertiaRatio=0.6,
                 filterByConvexity=False, minConvexity=0.87, maxConvexity=0.95):
        super().__init__(minThreshold, maxThreshold, thresholdStep,
                         filterByColor, blobColor,
                         filterByArea, minArea, maxArea,
                         filterByCircularity, minCircularity, maxCircularity,
                         filterByInertia, minInertiaRatio, maxInertiaRatio,
                         filterByConvexity, minConvexity, maxConvexity)

class CircleBlobDetector(BlobDetector):
    def __init__(self, params: CircleBlobParams):
        # Creates detector and drawParams and detectParams
        super().__init__(params)
    
    def detect(self, img):
        # Detect blobs in the image
        keypoints = self.detector.detect(img)
        return keypoints

    # TODO: parallelize this via merge sort method
    def drawKeypoints(self, img_to_draw_on, keypoints, drawParams):
        h, w = img_to_draw_on.shape[:2]
        
        overlay = img_to_draw_on.copy()

        # black background for grain mask
        line_mask = np.zeros((h, w, 3), dtype=np.uint8)

        # If no keypoints detected, return original image
        if len(keypoints) == 0:
            return img_to_draw_on

        seed = np.random.randint(0, 2**32 - 1)
        # draw tracking
        for kp in keypoints:
            x, y = int(kp.pt[0]), int(kp.pt[1])
            radius = int(kp.size / 2)

            # Draw keypoint on grain mask using white
            draw_circle(line_mask, (x,y), radius, drawParams, seed, no_grain=False)

            # Draw keypoint on overlay using color
            draw_circle(overlay, (x, y), radius, drawParams, seed)

        # TODO: draw tracking lines onto line_mask and overlay

        draw_tracking(line_mask, keypoints, drawParams, seed, no_grain=False)
        draw_tracking(overlay, keypoints, drawParams, seed)

        # Add grain to overlay lines
        add_grain(overlay, drawParams.grain)

        # Background = original image. On mask lines = overlay grained lines
        condition = line_mask > 0
        final = np.where(condition, overlay, img_to_draw_on)
        combined = np.hstack((img_to_draw_on, line_mask, overlay, final))
        return combined

    