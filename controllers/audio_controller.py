"""
audio_controller.py

Handles microphone input and speaker output.
Integrates speech recognition and text-to-speech capabilities.
"""

import pyaudio
import wave
import threading
import speech_recognition as sr
import pyttsx3
import time

class AudioController:
    def __init__(self):
        # Initialize PyAudio for input/output
        self.p = pyaudio.PyAudio()
        self.stream = None
        
        # Speech recognizer
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Text-to-speech engine
        self.tts_engine = pyttsx3.init()
        
        self.listening = False
        self.listening_thread = None
        self.callback = None  # Function to call when speech is recognized
    
    def start_listening(self, callback):
        """Start background listening to microphone and call callback(text) on recognized speech."""
        if self.listening:
            print("[AudioController] Already listening")
            return
        self.callback = callback
        self.listening = True
        self.listening_thread = threading.Thread(target=self._listen_in_background, daemon=True)
        self.listening_thread.start()
        print("[AudioController] Started listening")

    def _listen_in_background(self):
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
            while self.listening:
                print("[AudioController] Listening...")
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5)
                    text = self.recognizer.recognize_google(audio)
                    print(f"[AudioController] Recognized: {text}")
                    if self.callback:
                        self.callback(text)
                except sr.WaitTimeoutError:
                    print("[AudioController] Listening timeout, retrying...")
                except sr.UnknownValueError:
                    print("[AudioController] Could not understand audio")
                except sr.RequestError as e:
                    print(f"[AudioController] Recognition error: {e}")
                time.sleep(0.5)
    
    def stop_listening(self):
        """Stop the background listening thread."""
        self.listening = False
        if self.listening_thread:
            self.listening_thread.join()
        print("[AudioController] Stopped listening")
    
    def speak(self, text):
        """Speak given text out loud."""
        print(f"[AudioController] Speaking: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def cleanup(self):
        self.stop_listening()
        self.p.terminate()
        print("[AudioController] Cleaned up audio resources")
