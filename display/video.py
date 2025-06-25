from display.audio import *
from display.image import *

#TODO: try to prevent repeated renders

#TODO: multiple video in one frame (recursive) 
# layers: 


# image displayed for a # of beat intervals
class Frame():
    def __init__(self, image, num_beats=1):
        self.image = image
        self.num_beats = num_beats


# holds an audio
# list of frames
# processing: goes through list of frames, rendering audio accordingly
# based on each frame's # of beats

# Everything comes together
# Changes should be done individually to audio/frames, and then re-render video does all the video processing
class Video():
    def __init__(self, audio: Audio, frames: list[Frame]):
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

        # frame mapping to beats
        mapped_frames = []

        beat_num = 0
        frame_num = 0

        # iterate per frame
        while frame_num < len(self.frames) and beat_num < len(beats):
            frame = self.frames[frame_num]
            start_time = beats[beat_num]

            # Get duration based on frame
            if beat_num + frame.num_beats < len(beats):
                duration = beats[beat_num+frame.num_beats] - start_time
            else:
                duration = self.audio.duration_seconds - start_time

            print("VIDEO DURATION: ", duration)
            generated_image = frame.image.getRenderedImage()

            mapped_frames.append([generated_image, start_time, duration])
            frame_num += 1
            beat_num += frame.num_beats


        video_clips = []
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
    drawParams.grain = (-250, 255)  

    circleBlobDetector = CircleBlobDetector(circleBlobParams)

    circleBlobDetectorImage = SketchImage(circleBlobDetector, drawParams)

    baseImage.setChildren([overlayImage, overlayImage2,circleBlobDetectorImage])
    overlayImage.setChildren([circleBlobDetectorImage])

    baseImage.renderImage()
    renderImage = baseImage.getRenderedImage()

    
    # Resizing children

    # Resizing base

    # Moving children relatively

    print("DONE WITH IMAGE TESTS")