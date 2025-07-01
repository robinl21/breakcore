from blob_detection.circle import *
from draw_tools.draw_tools import *
from display.image import *
from display.audio import *
from display.video import *

import cv2
import numpy as np


def displayImage(img, title="Image"):
    """
    Displays an image in a window.
    """
    cv2.imshow(title, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# # TESTING IMAGE STACKING
# img = cv2.imread('samples/flash/images/ogwau.jpeg')

# Base Image:
baseImage = BaseImage('samples/flash/images/ogwau.jpeg', scale=1.0)

# # Basic render:
# renderImage = baseImage.getRenderedImage()

# displayImage(renderImage, "Base Image")

# # Base Image with another stacked on top

# # Overlay Image:
# overlayImage = OverlayImage('samples/flash/images/ogwau2.png')

# baseImage.setChildren([overlayImage])

# baseImage.renderImage()

# renderImage = baseImage.getRenderedImage()
# displayImage(renderImage, "Simple Image Stack")

# # Overlay Image 2:

# print("OVERLAY IMAGE 2")

# overlayImage2 = OverlayImage('samples/flash/images/ogwau3.png', cxPercent=0.25, cyPercent=0.25, scale=0.3)

# baseImage.setChildren([overlayImage, overlayImage2])
# baseImage.renderImage()
# renderImage = baseImage.getRenderedImage()

# displayImage(renderImage, "Image Two Stack")

# # Adding sketch
# # TODO: Be able to sketch on top of current render or original image
# print("SKETCHING \n")
# circleBlobParams = CircleBlobParams(keypointsKept=0.2)

# circleBlobParams.detectParams.minArea = 500

# drawParams = DrawParams()
# drawParams.thickness = 1
# drawParams.lineType = cv2.LINE_4
# drawParams.color = (255, 255, 255)
# drawParams.noise = (-10, 50)
# circleBlobDetector = CircleBlobDetector(circleBlobParams)

# circleBlobDetectorImage = BlobSketchImage(circleBlobDetector, drawParams)


# # Bug: drawing doesn't work with circleBlobDetector first...?
# baseImage.setChildren([overlayImage, overlayImage2,circleBlobDetectorImage])
# overlayImage.setChildren([circleBlobDetectorImage])

# baseImage.renderImage()
# renderImage = baseImage.getRenderedImage()

# displayImage(renderImage, "Sketch")

# Resizing children

# Resizing base

# Moving children relatively

# AUDIO
print("Running audio test cases...")
audio = Audio("samples/flash/audio/flash.wav", min_bpm=250, max_bpm=1000, fps=200)

beats = audio.render_beats()

print("Beats: ", beats)

audio.generate_click_audio()

print("Finish audio test cases")

# CONSTRUCT VIDEO

print("BEGIN VIDEO TEST CASES")
frames = []

for i in range(4,6):
    frameImg = BaseImage(f'samples/angel/frame_images/frame{i}.png')
    frame = Frame(frameImg, num_beats=1)
    frames.append(frame) 

for i in range(6, 13):  # 1 to 13 inclusive
    frameImg = BaseImage(f'samples/angel/frame_images/frame{i}.png')
    frame = Frame(frameImg, num_beats=2)
    frames.append(frame)


frameImg = BaseImage(f'samples/angel/frame_images/frame13.png')
frame = Frame(frameImg, num_beats=14)
frames.append(frame)

video = Video(audio, frames)

print("Generating video")
video.generate_video()


print("DONE WITH TESTS")