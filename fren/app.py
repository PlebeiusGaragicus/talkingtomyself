import os
import threading
import time
import json
import base64
import asyncio
from pathlib import Path

import pyaudio
import dotenv
import pygame
from pydub import AudioSegment
import assemblyai as aai
from openai import OpenAI


import logging
logger = logging.getLogger()

HERE = Path(__file__).parent


# Environment Check Function
def assert_env():
    if os.getenv("OPENAI_API_KEY", None) is None or os.getenv("ASSEMBLYAI_API_KEY", None) is None:
        logger.error("ENV vars not set in .env")
        exit(1)


# Audio Recording Class
class AudioRecorder:
    def __init__(self, format=pyaudio.paInt16, channels=1, rate=44100, chunk=1024):
        self.format = format
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.frames = []
        self.is_recording = False
        self.audio = pyaudio.PyAudio()
        self.stream = None

    def start_recording(self):
        self.is_recording = True
        self.stream = self.audio.open(format=self.format, channels=self.channels, 
                                      rate=self.rate, input=True, frames_per_buffer=self.chunk)
        while self.is_recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
        
        self.stream.stop_stream()
        self.stream.close()

    # def stop_recording(self):
    #     self.is_recording = False
    #     self.stream.stop_stream()
    #     self.stream.close()
    #     # self.audio.terminate()

    def save_recording(self, filename):
        sound = AudioSegment(data=b''.join(self.frames), sample_width=self.audio.get_sample_size(self.format),
                             frame_rate=self.rate, channels=self.channels)
        sound.export(filename, format="mp3")



def main():
    dotenv.load_dotenv(HERE.parent / ".env")
    assert_env()

    pygame.init()
    pygame.mixer.init()

    # create a 400 x 400 pygame window
    pygame.display.set_caption("Fren")
    pygame.display.set_mode((400, 400))

    ready_tone = pygame.mixer.Sound("./bling.mp3")
    recorder = AudioRecorder()
    record_thread = None

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and not recorder.is_recording:
                    ready_tone.play()
                    time.sleep(0.2) #TODO get len and sleep for that amount
                    recorder.frames = []  # Clear previous frames
                    record_thread = threading.Thread(target=recorder.start_recording)
                    record_thread.start()
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT and recorder.is_recording:
                    recorder.is_recording = False
                    # recorder.stop_recording()
                    ready_tone.play()
                    record_thread.join(0.5)
                    logger.info("Saving recording...")
                    recorder.save_recording("user_recording.mp3")
                    transcription = transcribe_audio()
                    speak(transcription)

            elif event.type == pygame.QUIT:
                running = False

    pygame.quit()



def transcribe_audio():
    logger.info("Transcribing audio...")
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

    transcriber = aai.Transcriber()

    config = aai.TranscriptionConfig(speaker_labels=False)
    transcript = transcriber.transcribe("./user_recording.mp3", config)

    logger.debug(transcript.text)

    return transcript.text



def speak(input: str):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.audio.speech.create(
        model="tts-1",
        # voice="onyx",
        voice="echo",
        input=f"{input}"
    )

    speech_file_path = HERE / "tts.mp3"
    response.stream_to_file(speech_file_path)

    # play the file with pygame
    tts = pygame.mixer.Sound(speech_file_path)
    tts.play()
