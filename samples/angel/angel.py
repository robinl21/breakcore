from blob_detection.circle import *
from draw_tools.draw_tools import *
from display.image import *

from edge_detection.edge import *

import cv2
import numpy as np


if __name__ == "__main__":

    # python -m display.angel.angel


    # Base Image: White Grain
    standardWhite = StandardBlock((255, 255, 255), 1080, 1080, grain=(-50, 50))
    baseImage = BaseImage(standardWhite, scale=1.0, grain=(-50, 50))

    # Angel:
    angel = OverlayImage('samples/angel/images/angel.png')

    # Angel Edge Detector for winged outline
    angelEdgeParams = OutlineParams(threshold1=50, threshold2=150)
    angelEdgeDetector = EdgeDetector(angelEdgeParams)

    # Angel Threshold Detector to fill in outline for a "messy" look
    angelThresholdParams = OutlineParams(is_threshold=True)
    angelThresholdDetector = EdgeDetector(angelThresholdParams)

    # Drawing Parameters for edge versus infill
    angelDrawParams = DrawParams(color=(242, 66, 245), thickness=-1)
    angelDrawParamsThreshold = DrawParams(color=(0, 0, 0), thickness=-1)
    
    # Render images
    angelEdgeImage = EdgeSketchImage(angel.getRenderedImage(), angelEdgeDetector, angelDrawParams, scale=1.5, grain=(-100, 100))
    angelThresholdImage = EdgeSketchImage(angel.getRenderedImage(), angelThresholdDetector, angelDrawParamsThreshold, scale=1.5, grain=(-100,100))
    
    # Overlay images on top of base image
    baseImage.setChildren([angelThresholdImage, angelEdgeImage])
    renderAndDisplay(baseImage, "Angel")

    madoka = OverlayImage('samples/angel/images/madoka.jpeg')
    madokaRotate = OverlayImage('samples/angel/images/madoka_rotate.png')
    
    madokaEdgeParams = OutlineParams(threshold1=50, threshold2=150)
    madokaEdgeDetector = EdgeDetector(angelEdgeParams)
    madokaDrawParams = DrawParams(color=(242, 66, 245), thickness=-1)

    madokaEdgeImage = EdgeSketchImage(madoka.getRenderedImage(), madokaEdgeDetector, madokaDrawParams, cxPercent=0.15, scale=1, grain=(-200, 200))
    
    madokaThresholdParams = OutlineParams(is_threshold=True)
    madokaThresholdDetector = EdgeDetector(madokaThresholdParams)
    madokaThresholdDrawParams = DrawParams(color=(0, 0, 0), thickness=-1, offset=(5, 5))

    madokaThresholdImage = EdgeSketchImage(madoka.getRenderedImage(), madokaThresholdDetector, madokaThresholdDrawParams, cxPercent=0.15, scale=1, transparency=0.8)
    

    # TODO: tune to be less clean of a line
    madokaDrawParams2 = DrawParams(color=(0, 0, 0), thickness=3, offset=(15, 0))
    madokaEdgeImage2 = EdgeSketchImage(madoka.getRenderedImage(), madokaEdgeDetector, madokaDrawParams2, cxPercent=0.15, scale=1, grain=(-200, 200))
    

    blackBlock = StandardBlock((0, 0, 0), 1000, 500, (-1000, 1000))
    blackBase1 = OverlayImage(blackBlock, cxPercent=0.2)

    blackBlock2 = StandardBlock((0, 0, 0), 1600, 500, (-1000, 1000))
    blackBase2 = OverlayImage(blackBlock2, cxPercent=0.7)

    madokaDetailedDraw = DrawParams(color=(0, 0, 0), thickness=-1)
    madokaDetailed = OutlineParams(threshold1=200, threshold2 = 300, contourMode=cv2.RETR_LIST)
    madokaDetailedEdgeDetector = EdgeDetector(madokaDetailed)

    madokaDetailedImage = EdgeSketchImage(madoka.getRenderedImage(), madokaDetailedEdgeDetector, madokaDetailedDraw, cxPercent=0.25, scale=3, grain=(-200, 200))

    madokaAbstractDraw = DrawParams(color=(242,66,245), thickness=1, offset=(0, 0))
    madokaAbstract = OutlineParams(threshold1=1, threshold2=15, contourMode = cv2.RETR_TREE)
    madokaAbstractEdgeDetector = EdgeDetector(madokaAbstract)
    madokaDetailedImage2 = EdgeSketchImage(madoka.getRenderedImage(), madokaAbstractEdgeDetector, madokaAbstractDraw, cxPercent=0.999, cyPercent=0.55, scale=2.6, grain=(-200, 200))
    
    
    # turn sketch into edges
    bowImg = OverlayImage('samples/angel/images/sketch_texture.jpeg', scale=0.2)

    bowDrawParams = DrawParams(color=(0, 0, 255), thickness=-1)
    bowEdgeParams = OutlineParams(threshold1=225, threshold2=500, contourMode=cv2.RETR_EXTERNAL)

    bowEdgeDetector = EdgeDetector(bowEdgeParams)

    bowImage = EdgeSketchImage(bowImg.getRenderedImage(), bowEdgeDetector, bowDrawParams, cxPercent=0.2, scale=1, grain=(-200, 200))
    

    bowImgReflect = OverlayImage('samples/angel/images/sketch_texture_rotate.png', scale=0.2)

    bowImageReflect = EdgeSketchImage(bowImgReflect.getRenderedImage(), bowEdgeDetector, bowDrawParams, cxPercent=0.8, scale=1, grain=(-200, 200))
    

    starImg = OverlayImage('samples/angel/images/stars.png', scale=1)

    starDrawParams = DrawParams(color=(214, 214, 214), thickness=-1)
    starEdgeParams = OutlineParams(threshold1=250, threshold2=350, contourMode=cv2.RETR_EXTERNAL)

    starEdgeDetector = EdgeDetector(starEdgeParams)

    starEdgeImage = EdgeSketchImage(starImg.getRenderedImage(), starEdgeDetector, starDrawParams, scale=1, cxPercent=0.8, cyPercent=0.5, grain=(-400, 400))
    

    standardPink = StandardBlock(color=(242, 66, 245), height=50, width=250, grain=(-100, 100))
    pinkRow = OverlayImage(standardPink, cxPercent=0.4, cyPercent=0.36, scale=1, transparency=0.85)

    standardPink2 = StandardBlock(color=(242, 66, 245), height=425, width=50)
    pinkCol = OverlayImage(standardPink2, cxPercent=0.99, cyPercent=0.5, scale=4, transparency=0.85, grain=(-100, 100))
    pinkCol2 = OverlayImage(standardPink2, cxPercent=0.4, cyPercent=0.45, scale=1, transparency=0.85, grain=(-100, 100))


    baseImage.setChildren([pinkCol, blackBase1, blackBase2, pinkRow, angelThresholdImage, pinkCol2, madokaDetailedImage, angelEdgeImage, madokaEdgeImage, bowImage, starEdgeImage, bowImageReflect])
    renderAndDisplay(baseImage, "Angel")

    

    