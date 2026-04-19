# VoiceGPT-Assistant
🎙️ Assistente de Voz Inteligente - VoiceGPT Assistant

[](https://python.org)
[](https://openai.com)
[](https://docs.pytest.org/)

> **Converse com o ChatGPT usando apenas sua voz\!** \> Assistente virtual inteligente desenvolvido como projeto para o **Bootcamp Bradesco - Java Cloud Native (DIO)**, integrando **Speech-to-Text**, **IA Generativa** e **Text-to-Speech**.

-----

## ✨ Funcionalidades

  - 🎤 **Entrada por Voz**: Captura de áudio em tempo real via microfone.
  - 🧠 **Processamento Inteligente**: Respostas contextuais via API da OpenAI (GPT-3.5/4).
  - 🔊 **Resposta Falada**: Síntese de voz natural utilizando gTTS (Google Text-to-Speech).
  - 🧪 **Qualidade de Código**: Arquitetura modular com cobertura de testes automatizados.
  - ⚡ **Modo Contínuo**: Loop de conversação otimizado para interação fluida.

## 🛠️ Tecnologias & Arquitetura

O projeto foi construído seguindo princípios de **Programação Orientada a Objetos (POO)** e modularização:

| Componente | Tecnologia | Função |
|------------|------------|--------|
| **STT** | OpenAI Whisper | Transcrição de áudio de alta precisão. |
| **LLM** | OpenAI GPT-3.5 | Processamento e geração de respostas. |
| **TTS** | gTTS | Conversão de texto em fala. |
| **I/O Áudio** | PyAudio / FFmpeg | Gerenciamento de hardware e formatos de áudio. |
| **Testes** | Pytest | Validação da estrutura e integridade dos módulos. |

## 📁 Estrutura do Projeto

```text
voicegpt-assistant/
├── src/                # Código fonte (Classes de serviço)
├── test/               # Testes unitários automatizados
├── .env                # Variáveis de ambiente (API Keys)
├── main.py             # Ponto de entrada da aplicação
└── requirements.txt    # Dependências do projeto
```

## 🚀 Como Executar

### 1\. Preparação do Ambiente

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/voicegpt-assistant.git
cd voicegpt-assistant

# Crie e ative o ambiente virtual
python -m venv venv
./venv/Scripts/activate
```

### 2\. Configuração

Crie um arquivo `.env` na raiz do projeto:

```text
OPENAI_API_KEY=sua_chave_aqui
```

### 3\. Execução

```bash
# Para rodar o assistente
python main.py

# Para rodar os testes unitários
python -m pytest test/ -v
```

## 👨‍💻 Desenvolvedor

Projeto desenvolvido por **Rogério Carmo** como parte da formação técnica na **Digital Innovation One (DIO)**.

-----

*Este projeto é para fins educacionais. Certifique-se de ter créditos ativos na sua conta OpenAI para o funcionamento das APIs.*

-----
🙏 Agradecimentos

Digital Innovation One (DIO) - Plataforma de educação
OpenAI - Whisper e GPT
Google - Tecnologia gTTS

📞 Contato

Autor: Rogério Carmo
LinkedIn: https://www.linkedin.com/in/rogeriocarmo40/
Email: rogeriocarmo.ti@gmail.com
