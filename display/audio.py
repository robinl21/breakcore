from madmom.features.beats import RNNBeatProcessor, DBNBeatTrackingProcessor
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips

import librosa
import soundfile as sf
import numpy as np

# TODO: try to limit re-rendering of beats / click audio and stuff if no changes are made


"""
Audio processing

Currently use RNNBeatProcessor to get beat activations
THen uses DBNBeatTrackingProcessor to get beat times
"""
class Audio():
    def __init__(self, audio_file, fps, min_bpm=55, max_bpm=215):
        self.fps = fps
        self.min_bpm = min_bpm
        self.max_bpm = max_bpm
        self.audio_file = audio_file
        self.click_audio = None
        self.click_audio_file_path = None

        self.audio_series, self.sample_rate = librosa.load(audio_file)
        self.duration_seconds = librosa.get_duration(y=self.audio_series, sr=self.sample_rate)

        self.beats = None

    """
    Renders beats according to settings
    Returns list of start time per beat
    """
    def render_beats(self):
        proc = RNNBeatProcessor(fps=self.fps)
        activations = proc(self.audio_file)

        tracker = DBNBeatTrackingProcessor(fps=self.fps, min_bpm=self.min_bpm, max_bpm=self.max_bpm)

        self.beats = tracker(activations)
        return self.beats

    """
    Generates audio with click sounds at beats if beats are rendered
    Saves file path and file
    Returns name of new generated file
    """
    def generate_click_audio(self, click_audio_file_path=None):

        if self.beats is None:
            self.render_beats()
        
        if click_audio_file_path is None:
            self.click_audio_file_path = self.audio_file + "_with_clicks.wav"
        else:
            self.click_audio_file_path = click_audio_file_path

        # Generate click sounds at the detected beats
        clicks = librosa.clicks(times=self.beats, sr=self.sample_rate, length=len(self.audio_series))

        # Mix clicks with original audio
        mixed = self.audio_series + clicks

        # Save the new audio
        sf.write(self.click_audio_file_path, mixed, self.sample_rate)

        return self.click_audio_file_path

    def get_audio_clip(self, click=False):
        if click:
            if self.click_audio_file_path == None:
                raise ValueError("No click audio file path generated")
            return AudioFileClip(self.click_audio_file_path)
        else:
            return AudioFileClip(self.audio_file)
        

if __name__ == "__main__":
    print("Running audio test cases...")
    audio = Audio("samples/flash/audio/flash.wav", min_bpm = 200, max_bpm = 1000, fps=200)

    beats = audio.render_beats()

    print("Beats: ", beats)

    audio.generate_click_audio()

    print("Finish audio test cases")








