from blob_detection.circle import *
from draw_tools.draw_tools import *
from display.image import *

from edge_detection.edge import *

import cv2
import numpy as np


if __name__ == "__main__":

    # python -m display.nurture


    # Base Image of Wires:
    baseImage = BaseImage('samples/nurture/images/wire.jpeg', scale=2.0, grain=(-50, 50))

    # Basic render:
    renderImage = baseImage.getRenderedImage()

    displayImage(renderImage, "Base Image")

    # Grass space in center

    grass = OverlayImage('samples/nurture/images/space.jpeg', scale=0.8, transparency=0.9)


    # Grass Blob Detector
    grassBlobParams = CircleBlobParams(minThreshold=10, maxThreshold=100)
    grassBlobDetector = CircleBlobDetector(grassBlobParams)

    # Grass Drawing Parameters
    grassDrawParams = DrawParams()
    grassDrawParams.thickness=5
    grassDrawParams.color = (255, 255, 255)
    grassDrawParams.noise = (-100, 500)

    grassBlobSketchImage = BlobSketchImage(grass.getRenderedImage(), grassBlobDetector, grassDrawParams, grain=(-50, 50))
    grass.setChildren([grassBlobSketchImage])

    # Liminal chairs in center too
    chairs = OverlayImage('samples/nurture/images/chairs.jpeg', grain=(-100, 100), cxPercent=0.8, cyPercent=0.65, scale=1.2, transparency=0.9)
    
    # Chair Blob Detector
    chairBlobParams = CircleBlobParams(maxThreshold=180, keypointsKept=0.6)
    chairBlobDetector = CircleBlobDetector(chairBlobParams)

    # Chair Drawing Parameters
    chairDrawParams = DrawParams()
    chairDrawParams.thickness=1
    chairDrawParams.color = (255, 255, 255)
    chairDrawParams.noise = (-50, 10)

    chairBlobSketchImage = BlobSketchImage(chairs.getRenderedImage(), chairBlobDetector, chairDrawParams)
    chairs.setChildren([chairBlobSketchImage])

    # Spiral
    spiral = OverlayImage('samples/nurture/images/spiral.JPG', grain=(-100,100), cxPercent=0.14, cyPercent=0.2, scale=0.4, transparency=0.7)
    
    # Spiral Blob Detector
    spiralBlobParams = CircleBlobParams(minThreshold=160, maxThreshold=10000)
    spiralBlobDetector = CircleBlobDetector(spiralBlobParams)

    # Chair Drawing Parameters
    spiralDrawParams = DrawParams()
    spiralDrawParams.thickness=4
    spiralDrawParams.color = (255, 255, 255)
    spiralDrawParams.noise = (0, 0)

    spiralBlobSketchImage = BlobSketchImage(spiral.getRenderedImage(), spiralBlobDetector, spiralDrawParams)
    spiral.setChildren([spiralBlobSketchImage])

    # Splotches of blue sky
    sky_rect_low = OverlayImage('samples/nurture/images/cloud_rect.png', grain=(-100, 100), cxPercent=0.4, cyPercent=0.8, scale=1.5, transparency=0.8)
    sky_rect_high = OverlayImage('samples/nurture/images/cloud_rect.png', grain=(-100, 100), cxPercent=0.75, cyPercent=0.2, scale=1.5, transparency=0.8)
    
    sky_rect_vert = OverlayImage('samples/nurture/images/cloud_rect_vert.png', grain=(-100, 100), cxPercent=0.2, cyPercent=0.7, scale=1.5, transparency=0.8)
    
    sky_rect_vert2 = OverlayImage('samples/nurture/images/cloud_rect_vert.png', grain=(-100, 100), cxPercent=0.8, cyPercent=0.2, scale=1.5, transparency=0.8)
    sky_square = OverlayImage('samples/nurture/images/cloud_square.png', grain=(-100, 100), cxPercent=0.2, cyPercent=0.2, scale=1, transparency=0.8)

    sky_square2 = OverlayImage('samples/nurture/images/cloud_square.png', grain=(-100, 100), cxPercent=0.8, cyPercent=0.60, scale=1, transparency=0.5)
    baseImage.setChildren([sky_rect_vert2, grass, spiral, chairs, sky_rect_low, sky_rect_vert, sky_rect_high, sky_square, sky_square2])

    baseImage.renderImage()

    # Green Flowers
    flowerEdgeParams = EdgeParams()
    flowerEdgeDetector = EdgeDetector(flowerEdgeParams)

    # Flower Parameters
    flowerDrawParams = DrawParams()
    flowerDrawParams.thickness= 1
    flowerDrawParams.color = (228, 179, 117)

    print("Flower edge sketch image")
    flowerEdgeSketchImage = EdgeSketchImage(baseImage.getRenderedImage(), flowerEdgeDetector, flowerDrawParams, grain=(-100, 100), transparency=1)


    baseImage.setChildren([sky_rect_vert2, grass, spiral, chairs, sky_rect_low, sky_rect_vert, sky_rect_high, sky_square, sky_square2, flowerEdgeSketchImage])

    renderAndDisplay(baseImage)

    # finalImg = baseImage.getRenderedImage()

    # cv2.imwrite("samples/nurture/final.png", finalImg)


    