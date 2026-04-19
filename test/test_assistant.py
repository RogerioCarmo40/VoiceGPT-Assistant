import sys
import os
import pytest

# Esse bloco garante que o Python encontre a pasta 'src' para importar seus arquivos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# Importando as funções do seu projeto (ajuste os nomes se necessário)
# Exemplo: importando do arquivo chatgpt_client.py
try:
    from chatgpt_client import responder_com_chatgpt # Altere para o nome real da sua função
except ImportError:
    pass

def test_verificacao_ambiente():
    """Verifica se o pytest está lendo a pasta de testes corretamente"""
    assert True

def test_estrutura_arquivos_src():
    """Verifica se os arquivos principais existem na pasta src"""
    caminho_src = os.path.abspath(os.path.join(os.path.dirname(__file__), '../src'))
    arquivos = os.listdir(caminho_src)
    assert "assistant.py" in arquivos
    assert "audio_handler.py" in arquivos
    assert "chatgpt_client.py" in arquivos

def test_validacao_simples_texto():
    """Teste de lógica simples para garantir execução"""
    mensagem = "Olá, Assistant"
    assert len(mensagem) > 0