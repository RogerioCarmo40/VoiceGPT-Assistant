from gtts import gTTS
import os

class GTTSClient:
    def __init__(self, language="pt"):
        self.language = language

    def save(self, text, filename):
        tts = gTTS(text=text, lang=self.language)
        tts.save(filename)
        
    def speak(self, text):
        filename = "temp_response.mp3"
        self.save(text, filename)
        os.system(f"start {filename}") # No Windows usa 'start'