from display.audio import *
from display.image import *

#TODO: try to prevent repeated renders

#TODO: multiple video in one frame (recursive) 
# layers: 


"""
The background frame

Input takes in list of images or a video
The video will be split into images (based on fps used for rendering)

Images per beat needs to be consistent across all children.

List of images:
Each image gets (images per beat * number of beats) / (number of images)

Video:
video gets processed to result in a total of images per beat * number of beats


Children:
    each child frame starts on a beat, and has own duration
        upon rendering, also returns a list of Images that we overlay with the base images
        add as child to the respective images
"""
class BaseFrame():
    def __init__(self, baseSource, scale=1.0, grain=(0,0), transparency=1.0, images_per_beat=1, num_beats=1, hardset_frames=None):
        self.baseSource = baseSource
        self.images_per_beat = images_per_beat
        self.num_beats = num_beats
        self.total_images = images_per_beat * num_beats
        self.hardset_frames = hardset_frames

        self.scale = scale
        self.grain = grain
        self.transparency = transparency

        self.children = []

        self.images = []

    def handleSource(self):
        self.images = []

        # processing list of base images
        if isinstance(self.baseSource, list):
            frames_to_use = self.total_images

            if self.hardset_frames != None:
                frames_to_use = self.hardset_frames
            
            k, m = divmod(frames_to_use, len(self.baseSource))

            num_copies = frames_to_use // len(self.baseSource)

            # need to make copies
            for i, img in enumerate(self.baseSource):
                # use min(i+1, m) to distribute the remaining m copies
                for j in range(num_copies + min(i+1, m)):
                    self.images.append(img.makeCopy())

            print("images after image as a list source handling: ", len(self.images))
        else:
            # is video: load and convert to array of self.total_images images
            # evenly spaced across video
            vid = cv2.VideoCapture(self.baseSource)

            if not vid.isOpened():
                print("Error: Cannot open video.")
                return
            
            total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

            if self.total_images > total_frames:
                raise ValueError("Requested more frames %d than what is available in video %d", self.total_images, total_frames )
            
            # array of evenly spaced numbers over specified interval
            # last one gets corrupt sometimes

            frames_to_use = total_frames
            if self.hardset_frames != None:
                frames_to_use = self.hardset_frames
            
            frame_indices = np.linspace(0, frames_to_use, num=self.total_images, dtype=int)

            last_valid_frame = 0
            for idx in frame_indices:
                vid.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = vid.read()

                if ret:
                    # turn to BaseImages
                    baseImage = BaseImage(frame, self.scale, self.grain)
                    self.images.append(baseImage)
                    last_valid_frame = idx
                else:
                    # reuse past frame
                    print("ISSUE at frame ", idx, " using ", last_valid_frame)
                    vid.set(cv2.CAP_PROP_POS_FRAMES, last_valid_frame)
                    ret, frame = vid.read()
                    baseImage = BaseImage(frame, self.scale, self.grain)

                    self.images.append(baseImage)
    
                    

            vid.release()

    def setChildren(self, children):
        self.children = children

    def getShape(self):
        self.handleSource()

        self.images[0].renderImage()
        return self.images[0].getRenderedImage().shape

    """
    Updates self.images
    """
    def compileFrameImages(self):

        # fills up self.images accordingly with BaseImages
        self.handleSource()

        for child in self.children:

            start_beat = child.start_beat
            child_num_beats = child.num_beats

            start_img_idx = start_beat * self.images_per_beat
            end_img_idx = start_img_idx + child_num_beats * self.images_per_beat # 1 past the actual number

            if child.images_per_beat != self.images_per_beat:
                raise ValueError("Child frames cannot be rendered on top because images per beat don't match. child: %d, us: %d", child.images_per_beat, self.images_per_beat)
                
            if start_img_idx > self.total_images:
                raise ValueError("Child frames cannot be rendered on top because start img index is greater than total images")
            if end_img_idx > self.total_images:
                raise ValueError("Child frames cannot be rendered on top because end image index is bigger than total images. end: %d, total images: %d", end_img_idx, self.total_images)
                
            #pouplate child.images
            child.compileFrameImages()

            childIdx = 0

            print("stard indx, end indx, # of our images, # of child", start_img_idx, end_img_idx, len(self.images), len(child.images))
            for baseIdx in range(start_img_idx, end_img_idx):
                self.images[baseIdx].addChild(child.images[childIdx])

                childIdx += 1



class OverlayFrame(BaseFrame):
    """
    Images per beat should be the same as the BaseFrame's
    """
    def __init__(self, baseSource, cxPercent=0.5, cyPercent=0.5, scale=0.5, grain=(0,0), transparency=1.0, images_per_beat=1, num_beats=2, start_beat=0, hardset_frames=None):
        super().__init__(baseSource, scale, grain, transparency, images_per_beat, num_beats, hardset_frames)

        self.cxPercent = cxPercent
        self.cyPercent = cyPercent
        self.start_beat = start_beat

        print("images per beat: ", images_per_beat)

class BlobSketchFrame(OverlayFrame):
    def __init__(self, baseSource, sketchTool, drawParams, cxPercent=0.5, cyPercent=0.5, scale=1.0, grain=(0,0), transparency=1.0, images_per_beat=1, num_beats=2, start_beat=0, hardset_frames=None):
        super().__init__(baseSource, cxPercent, cyPercent, scale, grain, transparency, images_per_beat, num_beats, start_beat, hardset_frames)
        self.sketchTool = sketchTool
        self.drawParams = drawParams
        print("images per beat: ", images_per_beat)

    def handleSource(self):
        self.images = []
        if isinstance(self.baseSource, list):
            pass
        else:
            # is video: load and convert to array of self.total_images images
            # evenly spaced across video
            vid = cv2.VideoCapture(self.baseSource)

            if not vid.isOpened():
                print("Error: Cannot open video.")
                return
            
            total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

            if self.total_images > total_frames:
                raise ValueError("Requested more frames %d than what is available in video %d", self.total_images, total_frames )
            
            frames_to_use = total_frames
            if self.hardset_frames != None:
                frames_to_use = self.hardset_frames
                
            # array of evenly spaced numbers over specified interval
            frame_indices = np.linspace(0, frames_to_use, num=self.total_images, dtype=int)

            last_valid_frame = 0
            for idx in frame_indices:
                vid.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = vid.read()
                if ret:
                    # turn to BlobSketchImages
                    sketchImage = BlobSketchImage(frame, self.sketchTool, self.drawParams, self.cxPercent, self.cyPercent, self.scale, self.grain, self.transparency)
                    self.images.append(sketchImage)
                    last_valid_frame = idx
                else:
                    print("ISSUE")
                    print("ISSUE at frame ", idx, " using ", last_valid_frame)
                    # reuse past frame
                    vid.set(cv2.CAP_PROP_POS_FRAMES, last_valid_frame)
                    ret, frame = vid.read()
                    sketchImage = BlobSketchImage(frame, self.sketchTool, self.drawParams, self.cxPercent, self.cyPercent, self.scale, self.grain, self.transparency)
                    self.images.append(sketchImage)
            vid.release()

class EdgeSketchFrame(OverlayFrame):
    def __init__(self, baseSource, sketchTool, drawParams, cxPercent=0.5, cyPercent=0.5, scale=1.0, grain=(0,0), transparency=1.0, images_per_beat=1, num_beats=2, start_beat=0, hardset_frames=None):
        super().__init__(baseSource, cxPercent, cyPercent, scale, grain, transparency, images_per_beat, num_beats, start_beat, hardset_frames)
        self.sketchTool = sketchTool
        self.drawParams = drawParams
        print("images per beat: ", images_per_beat)

    def handleSource(self):
        self.images = []
        if isinstance(self.baseSource, list):
            pass
        else:
            # is video: load and convert to array of self.total_images images
            # evenly spaced across video
            vid = cv2.VideoCapture(self.baseSource)

            if not vid.isOpened():
                print("Error: Cannot open video.")
                return
            
            total_frames = int(vid.get(cv2.CAP_PROP_FRAME_COUNT))

            if self.total_images > total_frames:
                raise ValueError("Requested more frames %d than what is available in video %d", self.total_images, total_frames )
            
            frames_to_use = total_frames
            if self.hardset_frames != None:
                frames_to_use = self.hardset_frames

            # array of evenly spaced numbers over specified interval
            frame_indices = np.linspace(0, frames_to_use, num=self.total_images, dtype=int)

            last_valid_frame = 0
            for idx in frame_indices:
                vid.set(cv2.CAP_PROP_POS_FRAMES, idx)
                ret, frame = vid.read()
                if ret:
                    # turn to EdgeSketchImages
                    sketchImage = EdgeSketchImage(frame, self.sketchTool, self.drawParams, self.cxPercent, self.cyPercent, self.scale, self.grain, self.transparency)
                    self.images.append(sketchImage)
                    last_valid_frame = idx
                else:
                    print("ISSUE at frame ", idx, " using ", last_valid_frame)
                    # reuse past frame
                    vid.set(cv2.CAP_PROP_POS_FRAMES, last_valid_frame)
                    ret, frame = vid.read()
                    sketchImage = EdgeSketchImage(frame, self.sketchTool, self.drawParams, self.cxPercent, self.cyPercent, self.scale, self.grain, self.transparency)
                    self.images.append(sketchImage)


            vid.release()

    def compileFrameImages(self):

        # fills up self.images accordingly with EdgeSketch overlays
        self.handleSource()

        for child in self.children:

            start_beat = child.start_beat
            child_num_beats = child.num_beats

            start_img_idx = start_beat * self.images_per_beat
            end_img_idx = start_img_idx + child_num_beats * self.images_per_beat # 1 past the actual number

            if child.images_per_beat != self.images_per_beat or start_img_idx >= self.total_images or end_img_idx >= self.total_images:
                raise ValueError("Child frames cannot be rendered on top")

            childImgs = child.renderFrameImages()

            childIdx = 0
            for baseIdx in range(start_img_idx, end_img_idx):
                self.images[baseIdx].addChild(childImgs[childIdx])

                childIdx += 1

        print("num images after rendering edge and compiling: ", len(self.images))
# holds an audio
# list of frames
# processing: goes through list of frames, rendering audio accordingly
# based on each frame's # of beats

# Everything comes together
# Changes should be done individually to audio/frames, and then re-render video does all the video processing
class Video():
    def __init__(self, audio: Audio, frames: list[BaseFrame]):
        self.audio = audio
        self.frames = frames
        
    def generate_video(self, click=False, video_path=None):

        # Process beat - get beat intervals
        self.audio.render_beats()

        # Handle audio path based on click
        audio_clip = None
        audio_file = self.audio.audio_file
        
        # Generate file of audio with clicks, or just get original audio path
        if click:
            audio_file=self.audio.generate_click_audio()
            audio_clip = self.audio.get_audio_clip(click=True)
        else:
            audio_clip = self.audio.get_audio_clip()

        # Set video path
        if video_path==None:
            video_path=audio_file + "_video.mp4"

        beats = self.audio.beats

        all_images_nested_by_frame = []

        for frame in self.frames:
            frame.compileFrameImages()
            all_images_nested_by_frame.append(frame.images)

        # frame mapping to beats
        mapped_frames = []

        beat_num = 0
        frame_num = 0 

        # iterate per frame
        while frame_num < len(self.frames) and beat_num < len(beats):
            print("Frame num, beatnum: ", frame_num, beat_num)
            start_time = beats[beat_num]
            frame = self.frames[frame_num]

            # Get duration of frame
            print("NUM BEATS: ", frame.num_beats)
            if beat_num + frame.num_beats < len(beats):
                duration = beats[beat_num+frame.num_beats] - start_time
            else:
                print("GO PAST NUM BWEATS")
                duration = self.audio.duration_seconds - start_time

            frame_images = all_images_nested_by_frame[frame_num]
            duration_per_image = duration / len(frame_images)

            # Get duration of each image
            print("VIDEO DURATION: ", duration)
            print("IMAGE DURATION: ", duration_per_image)
            

            for frame_image in frame_images:
                print("rendering frame image")
                # previously was just compiling - no total render done
                frame_image.renderImage()
                mapped_frames.append([frame_image.getRenderedImage(), start_time, duration_per_image])
                start_time += duration_per_image

            print("done rendering frame image")
            frame_num += 1
            beat_num += frame.num_beats

        video_clips = []

        print("compiling video")
        for generated_image, start_time, duration in mapped_frames:
            # BGR to RGB
            generated_image_rgb = cv2.cvtColor(generated_image, cv2.COLOR_BGR2RGB)
            clip = ImageClip(generated_image_rgb).set_start(start_time).set_duration(duration)
            video_clips.append(clip)

        final_video = concatenate_videoclips(video_clips, method='compose')
        final_video = final_video.set_audio(audio_clip)

        final_video = final_video.set_duration(final_video.duration)
        final_video.write_videofile(video_path, fps=30)

if __name__ == "__main__":
    # python -m display.video

    # TESTING IMAGE STACKING
    img = cv2.imread('samples/flash/images/ogwau.jpeg')

    # Base Image:
    baseImage = BaseImage('samples/flash/images/ogwau.jpeg', scale=1.0)

    # Basic render:
    renderImage = baseImage.getRenderedImage()

    # Base Image with another stacked on top

    # Overlay Image:
    overlayImage = OverlayImage('samples/flash/images/ogwau2.png')

    baseImage.setChildren([overlayImage])

    baseImage.renderImage()

    renderImage = baseImage.getRenderedImage()

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

    circleBlobDetector = CircleBlobDetector(circleBlobParams)

    circleBlobDetectorImage = BlobSketchImage(circleBlobDetector, drawParams)

    baseImage.setChildren([overlayImage, overlayImage2,circleBlobDetectorImage])
    overlayImage.setChildren([circleBlobDetectorImage])

    baseImage.renderImage()
    renderImage = baseImage.getRenderedImage()

    
    # Resizing children

    # Resizing base

    # Moving children relatively

    print("DONE WITH IMAGE TESTS")