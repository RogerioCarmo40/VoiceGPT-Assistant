import os
import sys
from dotenv import load_dotenv

# Garante que o Python encontre a pasta src
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# IMPORTAÇÃO CORRETA DAS CLASSES
from src.audio_handler import AudioHandler
from src.speech_recognition import WhisperRecognizer
from src.chatgpt_client import ChatGPTClient
from src.text_to_speech import GTTSClient

# Carrega as chaves do .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

def iniciar_assistente():
    # 1. Inicializa os componentes (Classes)
    handler = AudioHandler(sample_rate=16000)
    recognizer = WhisperRecognizer(api_key=api_key)
    chat_gpt = ChatGPTClient(api_key=api_key)
    tts = GTTSClient(language="pt")

    print("\n" + "="*40)
    print("   ASSISTENTE VOICE GPT ATIVADO")
    print("="*40)
    print("Pressione Ctrl+C para encerrar.\n")

    try:
        while True:
            # A. GRAVAÇÃO
            # O nome do arquivo onde salvaremos a voz temporariamente
            audio_temp = "input_usuario.wav"
            audio_data = handler.record(duration=5)
            handler.save(audio_data, audio_temp)

            # B. TRANSCRIÇÃO (Whisper)
            print("Entendendo sua voz...")
            texto_usuario = recognizer.transcribe(audio_temp)
            print(f"Você disse: {texto_usuario}")

            if not texto_usuario.strip():
                continue

            # C. INTELIGÊNCIA (ChatGPT)
            print("IA pensando na resposta...")
            resposta_ia = chat_gpt.chat(texto_usuario)
            print(f"IA respondeu: {resposta_ia}")

            # D. FALA (gTTS)
            tts.speak(resposta_ia)

    except KeyboardInterrupt:
        print("\n[LOG] Assistente encerrado pelo usuário.")
    except Exception as e:
        print(f"\n[ERRO] Ocorreu um problema: {e}")

if __name__ == "__main__":
    iniciar_assistente()