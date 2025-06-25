from blob_detection import *
from draw_tools.draw_tools import *

import cv2
import numpy as np

# Hierarchy in an image

"""
Image Hierarchy:


Scale of images are relative to the image provided.

Base Image: the background image, which can have overlays and blobs on top of it
    Overlay Image: an image that is rendered on top of the base image.
        Centered at a specific point relative to the base image size.
        If overlay image is bigger, cuts off.

Sketch Image:
    Same size as its parent (blob/tracking)
    Drawn over current state of rendering.

Changes called through functions, but not actually applied until rendering.
"""

# SketchImages: sketches on top of overlay images (from tools)


import cv2
import numpy as np

from abc import ABC, abstractmethod

class Image(ABC):
    def __init__():
        pass

"""
THe background image.

Input takes in jpgs, etc. -> converts into np array
Rendering is in pre-order traversal (in order of overlay children)

When making changes, changes don't apply until rendered
"""
class BaseImage(Image):
    def __init__(self, imgFile, scale=1.0):
        self.imgFile = imgFile

        # scale of base image is relative to given image
        self.scale = scale

        self.children = []

        # SHOULD NOT CHANGE AT ALL - only render changes
        self.curImage = self.fileToImage(imgFile)

        self.curRender = self.curImage.copy()  # Start with a copy of the current image for rendering

        self.renderImage() # Renders image to get currRender

    def fileToImage(self, imgFile):
        """
        Converts image file to np array
        """
        img = cv2.imread(imgFile, cv2.IMREAD_COLOR) 
        if img is None:
            raise ValueError(f"Could not read image file: {imgFile}")
        
        return img
    
    def resize_image(self, scale):
        """
        Resize base image to a new scale, without affecting children
        Args:
            scale (float): Scale factor to resize the image
        """
        self.scale = scale

    def resize_image_relative(self, relative_scale):
        """
        Resize base image proportionally, along with modifying base image scale of children
        """

        for overlay in self.children:
            if isinstance(overlay, OverlayImage):
                print("Resizing child")
                overlay.resize_image_relative(relative_scale)
        
        # resize ourselves
        self.resize_image(relative_scale * self.scale)

    def setChildren(self, children):
        """
        Sets children
        """
        self.children = children

    def changeBaseImage(self, newImgFile):
        """
        Modifies base child image
        """

        self.curImage = self.fileToImage(newImgFile)

    def getRenderedImage(self):
        """
        Returns copy of rendered image with all overlays applied
        """
        return self.curRender.copy()

    def renderImage(self):
        """
        Render the current image with all overlays applied and scale applied
        Sets cur_render
        """
        rendered = self.curImage.copy()

        # Resize the current image based on the new scale
        rendered = cv2.resize(rendered, None, fx=self.scale, fy=self.scale, interpolation=cv2.INTER_LINEAR)
        
        # Image dimensions
        lh, lw = rendered.shape[:2]

        for child in self.children:
            if isinstance(child, OverlayImage):

                print("Processing overlay image child \n")

                # Child renders itself first
                child.renderImage()

                childRender = child.getRenderedImage()

                # We add rendered child to us

                # Dimensions of overlay

                sh, sw = childRender.shape[:2]

                # Compute center for overlay
                x_center = int(lw * child.cxPercent)
                y_center = int(lh * child.cyPercent)

                
                # Compute bounds of overlay in base image
                x1_base = max(0, x_center - sw // 2)
                y1_base = max(0, y_center - sh // 2)
                x2_base= min(lw, x_center + sw // 2)
                y2_base = min(lh, y_center + sh // 2)

                # Compute corresponding region in overlay image
                # Logic: from center, try to go left by half.
                x1_src = max(0, -(x_center - sw // 2))
                y1_src = max(0, -(y_center - sh // 2))

                # 2base - 1base = width of overlay image needed while still being less than lw, lh
                x2_src = x1_src + (x2_base - x1_base)
                y2_src = y1_src + (y2_base - y1_base)

                if child.transparency == 1:
                    # Overlay: bound by lh, lw
                    rendered[y1_base:y2_base, x1_base: x2_base] = childRender[y1_src:y2_src, x1_src:x2_src]
                else:

                    print("Rendering transparent")
                    overlay_region = childRender[y1_src:y2_src, x1_src:x2_src]
                    base_region = rendered[y1_base:y2_base, x1_base: x2_base]

                    # Apply blending
                    blended_region = child.transparency * overlay_region + (1-child.transparency) * base_region

                    rendered[y1_base:y2_base, x1_base: x2_base] = blended_region[y1_src:y2_src, x1_src:x2_src]

            elif isinstance(child, SketchImage):
                print("SKETCH IMAGE")
                rendered = child.sketchOnImage(rendered)

        self.curRender = rendered



class OverlayImage(BaseImage):
    def __init__(self, img, cxPercent=0.5, cyPercent=0.5, scale=0.5, transparency=1.0):
        """
        cxPercent and cyPercent are relative to parent image size for center
        """
        super().__init__(img, scale)
        
        # center of overlay relative to parent image size
        self.cxPercent = cxPercent
        self.cyPercent = cyPercent
        self.transparency = transparency

    def reCenter(self, cxPercent, cyPercent):
        """
        Re-centers the overlay relative to parent image size
        Modifies cxPercent and cyPercent
        """
        self.cxPercent = cxPercent
        self.cyPercent = cyPercent

class SketchImage(Image):
    """
    Since sketches depend on the parent and previous siblings, sketch images are less of an image and more of a "command"{
    to add the sketch upon rendering
    """
    def __init__(self, sketchTool, drawParams):
        """
        Supported sketchTools: circleDetector instance
        """
        self.sketchTool = sketchTool
        self.drawParams = drawParams

    def sketchOnImage(self, imgToSketchOn):
        """
        Returns copy of imgToSketchOn with sketch.
        does not modify imgToSketchOn
        """
        # Use the sketch tool to draw on the image
        keypoints = self.sketchTool.detect(imgToSketchOn)
        newImage = self.sketchTool.drawKeypoints(imgToSketchOn, keypoints, self.drawParams)
        return newImage

def displayImage(img, title="Image"):
    """
    Displays an image in a window.
    """
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 

def renderAndDisplay(img: Image, title="image"):
    """
    Renders and displays image
    """
    img.renderImage()
    renderedImage = img.getRenderedImage()
    displayImage(renderedImage, title)

if __name__ == "__main__":

    # python -m display.image

    # TESTING IMAGE STACKING
    img = cv2.imread('samples/flash/images/ogwau.jpeg')

    # Base Image:
    baseImage = BaseImage('samples/flash/images/ogwau.jpeg', scale=1.0)

    # Basic render:
    renderImage = baseImage.getRenderedImage()

    displayImage(renderImage, "Base Image")

    # Base Image with another stacked on top

    # Overlay Image:
    overlayImage = OverlayImage('samples/flash/images/ogwau2.png', transparency=0.5)

    baseImage.setChildren([overlayImage])

    baseImage.renderImage()

    renderImage = baseImage.getRenderedImage()
    displayImage(renderImage, "Simple Image Stack")

    # Overlay Image 2:

    print("OVERLAY IMAGE 2")

    overlayImage2 = OverlayImage('samples/flash/images/ogwau3.png', cxPercent=0.25, cyPercent=0.25, scale=0.3)

    baseImage.setChildren([overlayImage, overlayImage2])
    baseImage.renderImage()
    renderImage = baseImage.getRenderedImage()

    displayImage(renderImage, "Image Two Stack")

    # Adding sketch
    # TODO: Be able to sketch on top of current render or original image
    print("SKETCHING \n")
    circleBlobParams = CircleBlobParams(keypointsKept=0.2)

    circleBlobParams.detectParams.minArea = 500

    drawParams = DrawParams()
    drawParams.thickness = 1
    drawParams.lineType = cv2.LINE_4
    drawParams.color = (255, 255, 255)
    drawParams.noise = (-10, 50)
    drawParams.grain = (-250, 255)  

    circleBlobDetector = CircleBlobDetector(circleBlobParams)

    circleBlobDetectorImage = SketchImage(circleBlobDetector, drawParams)

    baseImage.setChildren([overlayImage, overlayImage2,circleBlobDetectorImage])
    overlayImage.setChildren([circleBlobDetectorImage])

    baseImage.renderImage()
    renderImage = baseImage.getRenderedImage()

    displayImage(renderImage, "Sketch")

    # Resizing children

    print("Doubling size")
    baseImage.resize_image_relative(2)

    renderAndDisplay(baseImage)

    # Moving children relatively

    overlayImage2.reCenter(0.7,0.3)
    renderAndDisplay(baseImage)

    print("DONE WITH IMAGE TESTS")