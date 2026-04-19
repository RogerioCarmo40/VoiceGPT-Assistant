"""
VoiceGPT Assistant - Assistente de Voz Inteligente

Um sistema de conversação por voz que integra:
- OpenAI Whisper (Speech-to-Text)
- OpenAI GPT (Processamento de Linguagem)
- Google TTS (Text-to-Speech)
"""

__version__ = "1.0.0"
__author__ = "Seu Nome"
__license__ = "MIT"

from .assistant import VoiceAssistant
from .audio_handler import AudioHandler
from .speech_recognition import WhisperRecognizer
from .chatgpt_client import ChatGPTClient
from .text_to_speech import GTTSClient

__all__ = [
    "VoiceAssistant",
    "AudioHandler", 
    "WhisperRecognizer",
    "ChatGPTClient",
    "GTTSClient",
]