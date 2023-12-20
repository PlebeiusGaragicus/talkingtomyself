# from pynput import keyboard
# import pyaudio
# import wave

# # Audio setup
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
# CHUNK = 1024
# audio = pyaudio.PyAudio()
# stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
# frames = []

# # Control flags
# is_recording = False

# # Callback for key press
# def on_press(key):
#     global is_recording, frames
#     if key == keyboard.Key.f9:  # Choose the key for starting/stopping
#         if not is_recording:
#             is_recording = True
#             frames = []
#             print("Recording started...")
#         else:
#             is_recording = False
#             print("Recording stopped...")
#             stream.stop_stream()
#             stream.close()
#             audio.terminate()
#             # Save the recorded audio
#             with wave.open('output.wav', 'wb') as wf:
#                 wf.setnchannels(CHANNELS)
#                 wf.setsampwidth(audio.get_sample_size(FORMAT))
#                 wf.setframerate(RATE)
#                 wf.writeframes(b''.join(frames))
#             print("File saved.")
#             return False  # Returning False to stop the listener

# # Record audio
# def record():
#     global is_recording, frames
#     while is_recording:
#         data = stream.read(CHUNK)
#         frames.append(data)

# # Start listener
# with keyboard.Listener(on_press=on_press) as listener:
#     listener.join()

# # Start recording if key is pressed
# if is_recording:
#     record()




######### WAVE
# import os
# from pynput import keyboard
# import pyaudio
# import wave
# import threading

# from pathlib import Path
# HERE = Path(__file__).parent

# # Audio setup
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
# CHUNK = 1024
# audio = pyaudio.PyAudio()

# # Control flags and frame storage
# is_recording = False
# frames = []

# # Recording function
# def record_audio():
#     global is_recording, frames, stream
#     stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
#     while is_recording:
#         data = stream.read(CHUNK)
#         frames.append(data)

# # Key press event handler
# def on_press(key):
#     global is_recording, frames
#     if key == keyboard.Key.cmd:  # Change key as needed
#         if not is_recording:
#             is_recording = True
#             frames = []
#             threading.Thread(target=record_audio).start()
#             print("Recording started...")
#         # else:
#             # is_recording = False
#             # print("Stopping recording...")

# def on_release(key):
#     if is_recording and key == keyboard.Key.cmd:
#         print("Recording stopped. Saving file...")
#         stream.stop_stream()
#         stream.close()
#         audio.terminate()
#         with wave.open('output.wav', 'wb') as wf:
#             wf.setnchannels(CHANNELS)
#             wf.setsampwidth(audio.get_sample_size(FORMAT))
#             wf.setframerate(RATE)
#             wf.writeframes(b''.join(frames))
#         print("File saved.")

#         os.system(f"afplay {HERE / 'output.wav'}")
#         return False  # Stop listener

# # Start listener
# listener = keyboard.Listener(on_press=on_press, on_release=on_release)
# listener.start()
# listener.join()





import os
from pynput import keyboard
import pyaudio
import wave
import threading
from pydub import AudioSegment

from pathlib import Path
HERE = Path(__file__).parent

# Audio setup
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
audio = pyaudio.PyAudio()

# Control flags and frame storage
is_recording = False
frames = []

# Recording function
def record_audio():
    global is_recording, frames, stream
    stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
    while is_recording:
        data = stream.read(CHUNK)
        frames.append(data)

# Convert and save audio
def save_audio():
    sound = AudioSegment(
        data=b''.join(frames),
        sample_width=audio.get_sample_size(FORMAT),
        frame_rate=RATE,
        channels=CHANNELS
    )
    sound.export("output.mp3", format="mp3")
    print("MP3 file saved.")

# Key press event handler
def on_press(key):
    global is_recording, frames
    if key == keyboard.Key.cmd:  # Change key as needed
        if not is_recording:
            is_recording = True
            frames = []
            threading.Thread(target=record_audio).start()
            print("Recording started...")
        # else:
            # is_recording = False
            # print("Stopping recording...")

def on_release(key):
    if is_recording and key == keyboard.Key.cmd:
        print("Recording stopped. Saving file...")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        save_audio()
        print("File saved.")

        os.system(f"afplay {HERE / 'output.mp3'}")
        return False  # Stop listener


print("Press cmd to start recording.")
# Start listener
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()
listener.join()
