import cv2
import numpy as np

class EdgeParams():
    def __init__(self, contourMode=cv2.RETR_EXTERNAL, contourMethod=cv2.CHAIN_APPROX_NONE, blur=True):
        self.mode = contourMode
        self.method = contourMethod
        self.blur = blur

class OutlineParams(EdgeParams):
    def __init__(self, is_threshold=False, threshold1=50, threshold2=150, apertureSize=3, L2Gradient=False, contourMode=cv2.RETR_EXTERNAL, contourMethod=cv2.CHAIN_APPROX_NONE, blockSize = 21, C=10, blur=True):
        
        # MODES: cv2.RETR_LIST (retrieves all), cv2.RETR_EXTERNAL (only external), cv2.RETR_CCOMP (two-hierarchy), cv2.RETR_TREE (tree hierarchy)
        
        # lower threshold2 for sensitivity

        super().__init__(contourMode, contourMethod, blur)

        self.is_threshold=is_threshold

        # Canny edge detection specific

        # use higher low thresholds if you want to fill in for the shadow effect
        self.threshold1 = threshold1
        self.threshold2 = threshold2
        self.apertureSize = apertureSize
        self.L2Gradient = L2Gradient

        # Threshold specific
        # Threshold is calculated based on local neighborhood during edge detection
        # small blocksize = sensitive to local changes, large = smoother over large area
        # small C = more sensitive, large C = less sensitive, fewer pixels
        # size of pixel neighborhood to calculate threshold
        
        # to smooth out, use larger blocksize: 21 and 10
        self.blockSize = blockSize

        # constact subtracted from mean or weighted sum
        self.C = C
class EdgeDetector():
    def __init__(self, params: OutlineParams):
        self.params = params
    
    def get_contours(self, imgArr):
        imgArr = cv2.cvtColor(imgArr, cv2.COLOR_BGR2GRAY)
        if self.params.blur:
            imgArr = cv2.GaussianBlur(imgArr, (5, 5), 1.4)
        
        edges = None
        if self.params.is_threshold:
            # Use adaptive thresholding to capture the whole shape
            thresh = cv2.adaptiveThreshold(imgArr, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                    cv2.THRESH_BINARY_INV, self.params.blockSize, self.params.C)

            # Close gaps (larger kernel)
            kernel = np.ones((7, 7), np.uint8)
            edges = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            print("Process threshold")
        else:
            edges = cv2.Canny(imgArr, self.params.threshold1, self.params.threshold2, apertureSize=self.params.apertureSize, L2gradient=self.params.L2Gradient)
            
            # Close small gaps
            kernel = np.ones((5, 5), np.uint8)
            edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
        
        contours, _ = cv2.findContours(edges, self.params.mode, self.params.method)

        # gives detected contours - numpy array of points that describe boundary (N, 1, 2) each
        # N = number of points in contour, ...
        return contours
    
    """
    Use drawParams.thickness = -1 to fill
    """
    def getSketchTemplate(self, img_to_draw_on, contours, drawParams):
        h, w = img_to_draw_on.shape[:2]
        overlay = img_to_draw_on.copy()

        # black background for mask
        line_mask = np.zeros((h, w, 3), dtype=np.uint8)

        closed_contours = []

        if drawParams.thickness == -1 and self.params.is_threshold:
            for i, cnt in enumerate(contours):
                if not np.array_equal(cnt[0], cnt[-1]):
                    # Properly reshape the first point
                    first_point = cnt[0].reshape(1, 1, 2)
                    cnt = np.vstack([cnt, first_point])
                closed_contours.append(cnt)
        else:
            closed_contours = contours

        for idx, _ in enumerate(closed_contours):
            cv2.drawContours(overlay, closed_contours, idx, drawParams.color, thickness=drawParams.thickness, lineType=drawParams.lineType, offset=drawParams.offset)
            cv2.drawContours(line_mask, closed_contours, idx, (255, 255, 255), thickness=drawParams.thickness, lineType=drawParams.lineType, offset=drawParams.offset)
        
        return overlay, line_mask
