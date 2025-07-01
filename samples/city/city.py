from blob_detection import *
from draw_tools.draw_tools import *
from display.image import *
from display.video import *

from edge_detection.edge import *
import cv2
import numpy as np


if __name__ == "__main__":

    # python -m display.city

# nyc (subway run + People hanging on subways) +     # sf (train into water + people and streetcars + tokyo (shibuya) + triple s

    # subway run (one)
    baseFrame1 = BaseFrame('samples/city/video/subway_run_first_part.mp4', images_per_beat=4, num_beats=8)
    
    blobParams1 = CircleBlobParams(minThreshold=200, maxThreshold=400, keypointsKept=1)
    blobDetector1 = CircleBlobDetector(blobParams1)

    # Drawing Parameters
    blobDrawParams1 = DrawParams()
    blobDrawParams1.thickness=10
    blobDrawParams1.color = (0, 0, 0)
    blobDrawParams1.noise = (0, 0)

    blobSketchFrame1 = BlobSketchFrame('samples/city/video/subway_run.mp4', blobDetector1, blobDrawParams1, scale=1, images_per_beat=4, num_beats=8, grain=(-100,100))
    
    baseFrame1.setChildren([blobSketchFrame1])
    
    # subway hanging (two)
    # cut at 95 frames since can't process the rest right
    baseFrame2 = BaseFrame('samples/city/video/subway_hanging.mp4', images_per_beat=2, num_beats=8, hardset_frames=95)
    
    blobParams2 = CircleBlobParams(minThreshold=200, maxThreshold=400, keypointsKept=1)
    blobDetector2 = CircleBlobDetector(blobParams2)

    # Drawing Parameters
    blobDrawParams2 = DrawParams()
    blobDrawParams2.thickness=10
    blobDrawParams2.color = (0, 0, 0)
    blobDrawParams2.noise = (0, 0)

    blobSketchFrame2 = BlobSketchFrame('samples/city/video/subway_run.mp4', blobDetector2, blobDrawParams2, scale=1, images_per_beat=2, num_beats=8, grain=(-100,100), hardset_frames=95)
    
    baseFrame2.setChildren([blobSketchFrame2])
    

    # subway into water
    baseFrame3 = BaseFrame('samples/city/video/subway_water.mp4', images_per_beat=6, num_beats=8, hardset_frames=180)
    
    blobParams3 = CircleBlobParams(minThreshold=50, maxThreshold=100, keypointsKept=1)
    blobDetector3 = CircleBlobDetector(blobParams3)

    # Drawing Parameters
    blobDrawParams3 = DrawParams()
    blobDrawParams3.thickness=10
    blobDrawParams3.color = (0, 0, 0)
    blobDrawParams3.noise = (0, 0)

    blobSketchFrame3 = BlobSketchFrame('samples/city/video/subway_water.mp4', blobDetector3, blobDrawParams3, scale=1, images_per_beat=6, num_beats=8, grain=(-100,100), hardset_frames=180)
    
    baseFrame3.setChildren([blobSketchFrame3])
    
    print(baseFrame1.getShape()) #360, 640, 3)
    
    # hold that pose for me
    # baseFrame4 = BaseFrame('samples/city/video/willi_ninja.mp4', images_per_beat=2, num_beats=4)

    # # construct background blue image (SHOULD BE 360 640)
    blue = StandardBlock((141,124,89), 360, 640, grain=(-100, 100))
    blueImage = BaseImage("samples/city/images/water.png", 1)
    
    print(blueImage.getRenderedImage().shape)
    baseFrame4 = BaseFrame([blueImage], scale=0.8, images_per_beat=2, num_beats=6)

    edgeParams4 = OutlineParams(is_threshold=True, blockSize=31, C=12)
    edgeDetector4 = EdgeDetector(edgeParams4)

    # Drawing Parameters

    edgeDrawParams4 = DrawParams(color=(255, 255, 255))
    edgeDrawParams4.thickness=-1
    edgeDrawParams4.color = (0, 0, 0)
    edgeDrawParams4.noise = (0, 0)

    edgeSketchFrame4 = EdgeSketchFrame('samples/city/video/pose.mov', edgeDetector4, edgeDrawParams4, scale=0.4, images_per_beat=2, num_beats=6, grain=(-100,100))
    

    blobParams4 = CircleBlobParams(minThreshold=100, maxThreshold=300, keypointsKept=1)
    blobDetector4 = CircleBlobDetector(blobParams4)

    # Drawing Parameters
    blobDrawParams4 = DrawParams(num_connections=0)
    blobDrawParams4.thickness=2
    blobDrawParams4.color = (255, 255, 255)
    blobDrawParams4.noise = (-25, 25)

    blobSketchFrame4 = BlobSketchFrame('samples/city/video/pose.mov', blobDetector4, blobDrawParams4, scale=0.4, images_per_beat=2, num_beats=6, grain=(-100,100))
    baseFrame4.setChildren([blobSketchFrame4, edgeSketchFrame4])
    # overlay edge sketch

    # frame 5: BALL
    ballImage = BaseImage("samples/city/images/ball.png", scale=0.2)
    
    print(ballImage.getRenderedImage().shape)
    baseFrame5 = BaseFrame([ballImage], scale=0.8, images_per_beat=1, num_beats=1)

    # Frame 6: new york wandering with imprints

    # baseFrame = BaseFrame('samples/city/video/sf_street1.mp4', images_per_beat=6, num_beats=6)
    
     # Blob Detector
    # blobParams = CircleBlobParams(minThreshold=200, maxThreshold=400, keypointsKept=0.5)
    # blobDetector = CircleBlobDetector(blobParams)

    # # Drawing Parameters
    # blobDrawParams = DrawParams()
    # blobDrawParams.thickness=1
    # blobDrawParams.color = (0, 0, 0)
    # blobDrawParams.noise = (0, 0)

    # blobSketchFrame = BlobSketchFrame('samples/city/video/sf_street1.mp4', blobDetector, blobDrawParams, scale=1, images_per_beat=6, num_beats=6, grain=(-100,100))
    
    # baseFrame.setChildren([blobSketchFrame])
    

    # hold that pose for me (edge outline) - BEAT DROP ->  BALL


    # pose: 30:07 WILLI NINJA in BLUE on white background (atomrs core)
    
    # SECOND PART
    # BALL
    # monologue
    # taxis + people walking
    # Categories (song starts again)
    # taxis + people walking (sky/grass)
    # flash executive realness within it
    # WALL STREET RUNNING + FLASHING EXECUTIVE REALNESSS

    # THIRD PART
    # one.
    #  eusexua trailer intro word terms
    #  eusexua perfect stranger logo
    # EUSEXUA IS A MINDSET (at the end)

    # vampire weekend trailer

    # https://www.youtube.com/watch?v=Pdpg-1mw7E0&ab_channel=VampireWeekend


    # layer eusexua choreo over spielberg film


    # end with triple s scene (either falling or crow)
    # labels tracing - converges to euesxua logo

    # watched paris is burning - queer counterculture and resistance in the ballrooms
    # nyc 80s
    # 2:10https://www.youtube.com/watch?v=nI7EhpY2yaA&ab_channel=STATEOFDRESS
    
    # BALL at 3:53
    # poses at 4 (military)
    # 6:05 - it do take nerve
    # 6:44 - BALL is that very word - come and dress how you want to be

    # CATEGORIES
    # LUCIOUS BODY
    # SCHOOLBOY/SCHOOLGIRL REALNESS
    # TOWN AND COUNTRY
    # EXECUTIVE REALNESS
    # BUTCH QUEEN FIRST TIME..
    # HIGH FASHION EVENING REALNESS


    #end: 1:07

    # abrupt cut into rupaul dancing?
    # https://slate.com/human-interest/2019/06/nelson-sullivan-videos-queer-new-york.html

    fka = Audio('samples/city/audio/final_cut.mov', fps=60, min_bpm=150, max_bpm = 1000)
    video = Video(fka, [baseFrame4])

    video.generate_video(click=False, video_path='samples/city/video/final.mp4')
    