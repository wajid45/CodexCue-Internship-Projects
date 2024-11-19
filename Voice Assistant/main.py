import speech_recognition as sr
import pyttsx3
import webbrowser
import datetime
import os
import sys
from gtts import gTTS
import playsound

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Set the properties for the voice engine (optional)
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume level (0.0 to 1.0)

def speak(text):
    """Use pyttsx3 to speak the text."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen to user's command using the microphone and return text."""
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)  # Adjusts for ambient noise
        audio = recognizer.listen(source)
    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio)  # Use Google API for speech recognition
        print(f"You said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        print("Sorry, the speech service is unavailable.")
        return None

def execute_command(command):
    """Execute actions based on the user's command."""
    if 'hello' in command:
        speak("Hello! How can I assist you today?")
    
    elif 'time' in command:
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M")
        speak(f"The current time is {current_time}")
    
    elif 'open' in command and 'browser' in command:
        speak("Opening browser...")
        webbrowser.open("https://www.google.com")
    
    elif 'weather' in command:
        speak("I can tell you the weather if you specify the location.")
        # You can add code to get weather via an API (e.g., OpenWeatherMap) here.
    
    elif 'quit' in command or 'exit' in command:
        speak("Goodbye!")
        sys.exit()  # Exit the program
    
    else:
        speak("Sorry, I don't understand that command.")

def main():
    """Main loop to listen and respond to commands."""
    speak("Hello, I am your voice assistant. How can I help you?")
    
    while True:
        command = listen()
        if command:
            execute_command(command)

if __name__ == "__main__":
    main()
