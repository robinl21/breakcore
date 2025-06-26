import cv2
import numpy as np

class EdgeParams():
    def __init__(self, threshold1=50, threshold2=150, apertureSize=3, L2Gradient=False, contourMode=cv2.RETR_EXTERNAL, contourMethod=cv2.CHAIN_APPROX_NONE, blur=True):
        
        self.threshold1 = threshold1
        self.threshold2 = threshold2
        self.apertureSize = apertureSize
        self.L2Gradient = L2Gradient
        self.mode = contourMode
        self.method = contourMethod
        self.blur = blur

class EdgeDetector():
    def __init__(self, params: EdgeParams):
        self.params = params

    def get_edges(self, imgArr):
        if self.params.blur:
            imgArr = cv2.GaussianBlur(imgArr, (5, 5), 1.4)
        
        edges = cv2.Canny(imgArr, self.params.threshold1, self.params.threshold2, apertureSize=self.params.apertureSize, L2gradient=self.params.L2Gradient)

        return edges
    
    def get_contours(self, edges):

        contours, _ = cv2.findContours(edges, self.params.mode, self.params.method)

        # gives detected contours - numpy array of points that describe boundary (N, 1, 2) each
        # N = number of points in contour, ...
        return contours
    
    def getSketchTemplate(self, img_to_draw_on, contours, drawParams):
        h, w = img_to_draw_on.shape[:2]
        overlay = img_to_draw_on.copy()

        # black background for mask
        line_mask = np.zeros((h, w, 3), dtype=np.uint8)

        cv2.drawContours(overlay, contours, -1, drawParams.color, drawParams.thickness, drawParams.lineType, offset=drawParams.offset)
        cv2.drawContours(line_mask, contours, -1, drawParams.color, drawParams.thickness, drawParams.lineType, offset=drawParams.offset)
        
        return overlay, line_mask