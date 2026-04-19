"""
Orquestrador principal do VoiceGPT Assistant.
Coordena os módulos de áudio, STT, GPT e TTS.
"""

import os
import json
import logging
from typing import Optional, Callable
from dotenv import load_dotenv

from .audio_handler import AudioHandler
from .speech_recognition import WhisperRecognizer
from .chatgpt_client import ChatGPTClient
from .text_to_speech import GTTSClient

# Carrega variáveis de ambiente
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class VoiceAssistant:
    """
    Assistente de voz completo que integra:
    - Gravação de áudio
    - Transcrição (Whisper)
    - Processamento (ChatGPT)
    - Síntese de voz (gTTS)
    """
    
    def __init__(
        self,
        openai_api_key: Optional[str] = None,
        language: str = 'pt',
        gpt_model: str = 'gpt-3.5-turbo',
        continuous_mode: bool = False,
        save_history: bool = True
    ):
        """
        Inicializa o assistente de voz.
        
        Args:
            openai_api_key: Chave API OpenAI (ou env OPENAI_API_KEY)
            language: Idioma principal (pt, en, es...)
            gpt_model: Modelo GPT a usar
            continuous_mode: Se True, mantém conversa ativa
            save_history: Salvar histórico de conversas
        """
        # Configurações
        self.api_key = openai_api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("API Key da OpenAI não fornecida")
        
        self.language = language
        self.continuous_mode = continuous_mode
        self.save_history = save_history
        
        # Inicializa componentes
        logger.info("🚀 Inicializando VoiceAssistant...")
        
        self.audio = AudioHandler(
            sample_rate=int(os.getenv('SAMPLE_RATE', 16000)),
            channels=int(os.getenv('CHANNELS', 1))
        )
        
        self.recognizer = WhisperRecognizer(api_key=self.api_key)
        
        self.gpt = ChatGPTClient(
            api_key=self.api_key,
            model=gpt_model,
            temperature=float(os.getenv('TEMPERATURE', 0.7))
        )
        
        self.tts = GTTSClient(
            language=language,
            slow=False
        )
        
        # Callbacks para eventos
        self.on_listening: Optional[Callable] = None
        self.on_thinking: Optional[Callable] = None
        self.on_speaking: Optional[Callable] = None
        
        logger.info("✅ VoiceAssistant pronto!")
    
    def listen(self, duration: float = 5.0) -> str:
        """
        Grava áudio e transcreve para texto.
        
        Args:
            duration: Segundos de gravação
            
        Returns:
            Texto transcrito
        """
        if self.on_listening:
            self.on_listening()
        
        # Grava
        audio_data = self.audio.record(duration)
        
        # Transcreve
        try:
            text = self.recognizer.transcribe(audio_data, language=self.language)
            return text
        except Exception as e:
            logger.error(f"Erro na transcrição: {e}")
            return ""
    
    def think(self, text: str) -> str:
        """
        Processa texto com GPT e retorna resposta.
        
        Args:
            text: Pergunta ou entrada do usuário
            
        Returns:
            Resposta do assistente
        """
        if self.on_thinking:
            self.on_thinking()
        
        try:
            response = self.gpt.chat(text)
            return response
        except Exception as e:
            logger.error(f"Erro no GPT: {e}")
            return "Desculpe, tive um problema ao processar sua pergunta."
    
    def speak(self, text: str):
        """
        Converte texto em fala e reproduz.
        
        Args:
            text: Texto a ser falado
        """
        if self.on_speaking:
            self.on_speaking()
        
        try:
            self.tts.speak(text)
        except Exception as e:
            logger.error(f"Erro no TTS: {e}")
            print(f"📝 Resposta: {text}")
    
    def process_cycle(self, duration: float = 5.0) -> dict:
        """
        Executa um ciclo completo: ouvir -> pensar -> falar.
        
        Args:
            duration: Segundos de gravação
            
        Returns:
            Dicionário com resultados de cada etapa
        """
        result = {
            'transcription': None,
            'response': None,
            'success': False
        }
        
        try:
            # 1. OUVIR
            print("\n🎤 Ouvindo... (fale agora)")
            transcription = self.listen(duration)
            
            if not transcription:
                print("❌ Não entendi. Poderia repetir?")
                return result
            
            print(f"📝 Você disse: '{transcription}'")
            result['transcription'] = transcription
            
            # Comandos especiais
            if transcription.lower() in ['sair', 'exit', 'quit', 'parar']:
                print("👋 Encerrando assistente...")
                result['success'] = True
                result['command'] = 'exit'
                return result
            
            if transcription.lower() in ['limpar', 'clear', 'novo']:
                self.gpt.clear_history()
                print("🧹 Conversa reiniciada")
                result['success'] = True
                result['command'] = 'clear'
                return result
            
            # 2. PENSAR
            print("🤖 Pensando...")
            response = self.think(transcription)
            result['response'] = response
            
            # 3. FALAR
            print(f"🔊 Resposta: '{response[:100]}...'" if len(response) > 100 else f"🔊 Resposta: '{response}'")
            self.speak(response)
            
            result['success'] = True
            
            # Salva histórico se necessário
            if self.save_history:
                self._save_interaction(transcription, response)
            
        except KeyboardInterrupt:
            print("\n⚠️ Interrompido pelo usuário")
            raise
        except Exception as e:
            logger.error(f"Erro no ciclo: {e}")
            print(f"❌ Erro: {e}")
        
        return result
    
    def run(self, cycles: Optional[int] = None):
        """
        Executa assistente em modo contínuo ou por N ciclos.
        
        Args:
            cycles: Número de ciclos (None = infinito se continuous_mode)
        """
        print(f"\n{'='*50}")
        print("🎙️  VoiceGPT Assistant")
        print(f"🌍 Idioma: {self.language}")
        print(f"🤖 Modelo: {self.gpt.model}")
        print(f"⚡ Pressione Ctrl+C para sair")
        print(f"{'='*50}\n")
        
        cycle_count = 0
        
        try:
            while True:
                if cycles and cycle_count >= cycles:
                    break
                
                self.process_cycle()
                cycle_count += 1
                
                if not self.continuous_mode and cycles is None:
                    break
                    
        except KeyboardInterrupt:
            print("\n\n👋 Assistente encerrado pelo usuário")
        finally:
            self.shutdown()
    
    def _save_interaction(self, question: str, answer: str):
        """Salva interação em histórico."""
        history_file = os.getenv('HISTORY_FILE', 'conversation_history.json')
        
        entry = {
            'timestamp': str(json.loads(json.dumps({'t': 'now'}))),  # Simplificado
            'question': question,
            'answer': answer
        }
        
        # Append ao arquivo
        try:
            if os.path.exists(history_file):
                with open(history_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            else:
                data = []
            
            data.append(entry)
            
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"Não foi possível salvar histórico: {e}")
    
    def shutdown(self):
        """Libera recursos."""
        self.audio.cleanup()
        if self.save_history:
            self.gpt.save_history('final_conversation.json')
        logger.info("🛑 Assistente finalizado")
    
    def __enter__(self):
        """Context manager."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup on exit."""
        self.shutdown()
        return False