# pip install SpeechRecognition, pyaudio


import speech_recognition as sr

# Initialize the recognizer
r = sr.Recognizer()

# Define a callback function to handle the recognized speech
def callback(recognized_text):
    print("Recognized:", recognized_text)

# Continuous listening and speech recognition
with sr.Microphone() as source:
    print("Adjusting for ambient noise. Please wait...")
    r.adjust_for_ambient_noise(source, duration=1)  # Adjust for ambient noise
    print("Now listening...")

    try:
        while True:  # Infinite loop to continuously listen
            audio = r.listen(source, phrase_time_limit=5)  # Listen for 5 seconds
            try:
                # Recognize speech using Google Web Speech API
                recognized_text = r.recognize_google(audio)
                callback(recognized_text)  # Send the recognized text to the callback
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print("Error; {0}".format(e))
    except KeyboardInterrupt:
        print("Listening stopped by user")

# Run this code in a terminal or script
