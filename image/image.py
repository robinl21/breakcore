# Hierarchy in an image

"""
Image Hierarchy:


Scale of images are relative to the image given.

Base Image: the background image, which can have overlays and blobs on top of it
    Overlay Image: an image that is rendered on top of the base image.
        Centered at a specific point relative to the base image size.
        If overlay image is bigger, cuts off.

Sketch Image:
    Same size as its parent (blob/tracking)
    Drawn over current state of rendering.

When rendering children, mutates current rendered image.
When giving rendered image to parent, returns copy (so parent does not mutate children directly)
When giving sketched image back to parent, returns copy
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
"""
class BaseImage(Image):
    def __init__(self, imgFile, scale=1.0):
        self.imgFile = imgFile

        # scale of base image is relative to given image
        self.scale = scale

        self.children = []

        self.curImage = self.fileToImage(imgFile)
        self.curRender = self.curImage.copy()  # Start with a copy of the current image for rendering

        self.resize_image(scale)  # Resize the image to the initial scale

    def fileToImage(self, imgFile):
        """
        Converts image file to np array
        """
        img = cv2.imread(imgFile, cv2.IMREAD_COLOR) 
        if img is None:
            raise ValueError(f"Could not read image file: {imgFile}")
        
        return img
    
    def getRenderedImage(self):
        """
        Returns copy of rendered image with all overlays applied
        """
        return self.curRender.copy()

    def renderImage(self):
        """
        Render the current image with all overlays applied
        MODIFIES CURRENDER image
        """
        rendered = self.curImage.copy()
        for overlay in self.children:
            rendered = cv2.addWeighted(rendered, 1.0, overlay.curRender, 0.5, 0)
        self.curRender = rendered
 

    def resize_image(self, scale):
        """
        Resize just the image to a new scale, without affecting children
        Modifies curRender and curImage
        Args:
            scale (float): Scale factor to resize the image
        """
        self.scale = scale

        # Resize the current image based on the new scale
        self.curImage = cv2.resize(self.curImage, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        
        # Re-render the image with the resized current image
        self.renderImage()

    def resize_image_relative(self, scale):
        """
        Resize the image relative to the current scale, along with modifying scale of children
        Modifies curRender and curImage
        """
        self.scale = scale
        for overlay in self.children:
            overlay.resize_image_relative(scale)
        # Resize the current image based on the new scale
        self.curImage = cv2.resize(self.curImage, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)

        # Re-render the image with the resized current image
        self.renderImage()

    def setOverlayChildren(self, overlayChildren):
        """
        Sets the overlay children of this base image
        Modifies overlayChildren and render image
        Args:
            overlayChildren (list): List of OverlayImage objects to set as children
        """
        self.overlayChildren = overlayChildren

        self.renderImage()

    def changeBaseImage(self, newImgFile):
        """
        Modifies base child image, re-renders.
        """

        self.curImage = self.fileToImage(newImgFile)
        self.curRender = self.curImage.copy()  # Start with a copy of the current image for rendering

        self.resize_image(self.scale)

        # Re-render the image with the new base image
        self.renderImage()



class OverlayImage(BaseImage):
    def __init__(self, img, cxPercent=0.5, cyPercent=0.5, scale=0.5):
        """
        cxPercent and cyPercent are relative to parent image size for center
        """
        super().__init__(img, scale)
        
        # center of overlay relative to parent image size
        self.cxPercent = cxPercent
        self.cyPercent = cyPercent

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
    def __init__(self, sketchTool):
        """
        Supported sketchTools: circleDetector instance
        """
        self.sketchTool = sketchTool


    def sketchOnImage(self, imgToSketchOn):
        """
        Returns copy of imgToSketchOn with sketch.
        does not modify imgToSketchOn
        """
        # Use the sketch tool to draw on the image
        self.sketchTool.draw(imgToSketchOn)
        return imgToSketchOn
