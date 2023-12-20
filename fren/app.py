import os
import threading
import time
import json
import base64
import asyncio
from pathlib import Path
import requests
from typing import Optional

import pyaudio
import dotenv
import pygame
from pydub import AudioSegment
import assemblyai as aai
from openai import OpenAI


import logging
logger = logging.getLogger()

HERE = Path(__file__).parent

OpenAIClient = None
# https://platform.openai.com/docs/guides/text-to-speech
OpenAIVoices = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']

# Environment Check Function
def assert_env():
    if os.getenv("OPENAI_API_KEY", None) is None or \
        os.getenv("ASSEMBLYAI_API_KEY", None) is None or \
            os.getenv("BASE_API_URL", None) is None or \
                os.getenv("FLOW_ID", None) is None:
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
        self.frames = []
        self.stream = self.audio.open(format=self.format, channels=self.channels, 
                                      rate=self.rate, input=True, frames_per_buffer=self.chunk)
        while self.is_recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
        
        self.stream.stop_stream()
        self.stream.close()
        # self.audio.terminate()

        sound = AudioSegment(data=b''.join(self.frames), sample_width=self.audio.get_sample_size(self.format),
                             frame_rate=self.rate, channels=self.channels)
        sound.export("user_recording.mp3", format="mp3")

        transcription = transcribe_audio()

        # input_dict = {"input": transcription, "user_name": "Micah"}
        input_dict = {"input": transcription}
        result = run_flow(input_dict, flow_id=os.getenv("FLOW_ID"), tweaks=TWEAKS)

        logger.info(result)

        try:
            speak(result['result']['output'])
        except KeyError:
            speak(f"Something is wrong with my code... {result['detail']}", voice=OpenAIVoices[3])



def main():
    dotenv.load_dotenv(HERE.parent / ".env")
    assert_env()

    pygame.init()
    pygame.mixer.init()

    # Set up the display
    screen_width, screen_height = 600, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Fren")

    font = pygame.font.Font(None, 40)

    ready_tone = pygame.mixer.Sound("./bling.mp3")
    recorder = AudioRecorder()
    record_thread = None

    global OpenAIClient
    OpenAIClient = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and not recorder.is_recording:
                    ready_tone.play()
                    time.sleep(0.2) #TODO get len and sleep for that amount
                    record_thread = threading.Thread(target=recorder.start_recording)
                    record_thread.start()

                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    running = False

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT and recorder.is_recording:
                    recorder.is_recording = False
                    # recorder.stop_recording()
                    ready_tone.play()
                    record_thread.join()

                    # transcription = transcribe_audio()

                    # input_dict = {"input": transcription}
                    # result = run_flow(input_dict, flow_id=os.getenv("FLOW_ID"), tweaks=TWEAKS)

                    # speak(result['result']['output'])

            elif event.type == pygame.QUIT:
                running = False

        ### END EVENT LOOP ###

        # Fill the screen with a color
        screen.fill((25, 55, 35))

        # Render the text
        text = font.render("Hold [SHIFT] to record your question!", True, (200, 200, 100))
        text_rect = text.get_rect(center=(screen_width/2, screen_height/2))
        screen.blit(text, text_rect)

        # Update the display
        pygame.display.flip()

    pygame.quit()



def transcribe_audio():
    logger.info("Transcribing audio...")
    aai.settings.api_key = os.getenv("ASSEMBLYAI_API_KEY")

    transcriber = aai.Transcriber()

    config = aai.TranscriptionConfig(speaker_labels=False)
    transcript = transcriber.transcribe("./user_recording.mp3", config)

    logger.debug(transcript.text)

    return transcript.text



def speak(input: str, voice = OpenAIVoices[4]):
    response = OpenAIClient.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=f"{input}"
    )

    speech_file_path = HERE / "tts.mp3"
    response.stream_to_file(speech_file_path)

    # play the file with pygame
    tts = pygame.mixer.Sound(speech_file_path)
    tts.play()






# You can tweak the flow by adding a tweaks dictionary
# e.g {"OpenAI-XXXXX": {"model_name": "gpt-4"}}
TWEAKS = {
  "OpenAIConversationalAgent-0HJdd": {},
  "PythonFunctionTool-uJfF3": {}
}

def run_flow(inputs: dict, flow_id: str, tweaks: Optional[dict] = None) -> dict:
    """
    Run a flow with a given message and optional tweaks.

    :param message: The message to send to the flow
    :param flow_id: The ID of the flow to run
    :param tweaks: Optional tweaks to customize the flow
    :return: The JSON response from the flow
    """
    api_url = f"{os.getenv('BASE_API_URL')}/{flow_id}"

    payload = {"inputs": inputs}
    headers = None
    if tweaks:
        payload["tweaks"] = tweaks
    response = requests.post(api_url, json=payload, headers=headers)

    # response = requests.post(api_url, json=payload, headers=headers, stream=True)
    # get each streamed event
    # for line in response.iter_lines():
    #     if line:
    #         decoded_line = line.decode('utf-8')
    #         event = json.loads(decoded_line)
    #         logger.info(event)

    logger.info(response.json())

    return response.json()
