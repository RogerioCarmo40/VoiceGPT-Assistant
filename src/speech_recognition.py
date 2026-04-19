from openai import OpenAI

class WhisperRecognizer:
    def __init__(self, api_key):
        self.client = OpenAI(api_key=api_key)

    def transcribe(self, audio_path, language="pt"):
        with open(audio_path, "rb") as audio_file:
            transcricao = self.client.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                language=language
            )
        return transcricao.text