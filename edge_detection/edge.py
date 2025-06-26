class EdgeParams():
    def __init__(self, minThreshold=100, maxThreshold=220, thresholdStep=10,
                 filterByColor=False, blobColor=0,
                 filterByArea=True, minArea=250, maxArea=10000,
                 filterByCircularity=False, minCircularity=0.1, maxCircularity=0.8,
                filterByInertia=False, minInertiaRatio=0.1, maxInertiaRatio=0.6,
                filterByConvexity=False, minConvexity=0.87, maxConvexity=0.95,
                keypointsKept=1.0):
        
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

        self.keypointsKept = keypointsKept