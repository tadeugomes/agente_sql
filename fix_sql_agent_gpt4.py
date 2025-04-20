"""
Este script corrige o problema com o ChatOpenAI no sql_agent.py.
Esta versão usa o modelo GPT-4 que suporta ferramentas (tool use).
"""

import re

def fix_sql_agent_file():
    try:
        # Ler o arquivo original
        with open('sql_agent.py', 'r') as file:
            content = file.read()
        
        # Fazer backup do arquivo original
        with open('sql_agent.py.bak', 'w') as file:
            file.write(content)
        
        # Substituir a inicialização do ChatOpenAI
        # Padrão antigo: model_kwargs={'headers': ...}
        # Novo padrão: sem headers e usando GPT-4
        old_code = """        # Inicializar o modelo usando OpenRouter
        llm = ChatOpenAI(
            model="deepseek/deepseek-v3-base:free",
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            model_kwargs={
                "headers": {
                    "HTTP-Referer": "http://localhost:8501",
                    "X-Title": "SQL Agent"
                }
            }
        )"""
        
        new_code = """        # Inicializar o modelo usando OpenRouter com GPT-4 que suporta ferramentas
        llm = ChatOpenAI(
            model="openai/gpt-4-turbo",  # Usando GPT-4 que suporta ferramentas
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1",
            default_headers={  # Usando default_headers em vez de model_kwargs
                "HTTP-Referer": "http://localhost:8501",
                "X-Title": "SQL Agent"
            }
        )"""
        
        # Substituir o código antigo pelo novo
        new_content = content.replace(old_code, new_code)
        
        # Atualizar o import do ChatOpenAI
        old_import = "from langchain_community.chat_models import ChatOpenAI"
        new_import = "from langchain_openai import ChatOpenAI  # Atualizado para usar langchain_openai"
        new_content = new_content.replace(old_import, new_import)
        
        # Escrever o conteúdo atualizado
        with open('sql_agent.py', 'w') as file:
            file.write(new_content)
        
        print("✅ Arquivo sql_agent.py atualizado com sucesso!")
        print("Um backup do arquivo original foi salvo como sql_agent.py.bak")
        print("\nAlterações realizadas:")
        print("1. Atualizado o import de ChatOpenAI para usar langchain_openai")
        print("2. Alterado o modelo para 'openai/gpt-4-turbo' que suporta ferramentas")
        print("3. Substituído model_kwargs={'headers': ...} por default_headers={...}")
        
    except Exception as e:
        print(f"❌ Erro ao atualizar o arquivo: {e}")

if __name__ == "__main__":
    fix_sql_agent_file()
