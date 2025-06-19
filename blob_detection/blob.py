
from abc import ABC, abstractmethod
import cv2
from draw_tools.draw_tools import DrawParams

# abstract base class for blob parameters
# For other blob detectors, inherit from BlobParams
class BlobParams(ABC):
    def __init__(self, minThreshold=100, maxThreshold=220, thresholdStep=10,
                 filterByColor=False, blobColor=0,
                 filterByArea=True, minArea=250, maxArea=10000,
                 filterByCircularity=False, minCircularity=0.1, maxCircularity=0.8,
                filterByInertia=False, minInertiaRatio=0.1, maxInertiaRatio=0.6,
                filterByConvexity=False, minConvexity=0.87, maxConvexity=0.95,
                drawColor=(0, 0, 255), drawThickness=2, drawLineType=cv2.LINE_AA, drawNoise=(0,0), drawGrain=(0,0)):
        
        detectParams = cv2.SimpleBlobDetector_Params()
        detectParams.minThreshold = minThreshold
        detectParams.maxThreshold = maxThreshold
        detectParams.thresholdStep = thresholdStep
        detectParams.filterByColor = filterByColor
        detectParams.blobColor = blobColor
        detectParams.filterByArea = filterByArea
        detectParams.minArea = minArea
        detectParams.maxArea = maxArea
        detectParams.filterByCircularity = filterByCircularity
        detectParams.minCircularity = minCircularity
        detectParams.maxCircularity = maxCircularity
        detectParams.filterByInertia = filterByInertia
        detectParams.minInertiaRatio = minInertiaRatio
        detectParams.maxInertiaRatio = maxInertiaRatio
        detectParams.filterByConvexity = filterByConvexity
        detectParams.minConvexity = minConvexity
        detectParams.maxConvexity = maxConvexity

        # Set the detection parameters
        self.detectParams = detectParams

        drawParams = DrawParams(drawColor, drawThickness, drawLineType, drawNoise, drawGrain)

        # Set the draw parameters
        self.drawParams = drawParams

# abstract base class for blob detector
#for other blob detectors, inherit from BlobDetector
class BlobDetector(ABC):
    def __init__(self, params:BlobParams):
        self.detectParams = params.detectParams
        self.drawParams = params.drawParams
        # Create a SimpleBlobDetector object with the specified parameters
        self.detector = cv2.SimpleBlobDetector_create(params.detectParams)
    """
    Detects blobs and returns list of keypoints
    """
    @abstractmethod
    def detect(self, img):
        pass

    """
    Draws keypoints according to drawParams
    """
    @abstractmethod
    def drawKeypoints(self, img, keypoints):
        pass
