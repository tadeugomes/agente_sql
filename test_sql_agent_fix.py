"""
Este script testa se o SQL Agent está funcionando corretamente após a correção.
"""

import os
from dotenv import load_dotenv
from sql_agent import SQLAgent

# Carregar variáveis de ambiente
load_dotenv()

# Verificar se a chave da API foi carregada corretamente
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    # Mascarar a chave para exibição segura - nunca exiba a chave completa
    # Não exibir nenhuma parte da chave real, apenas indicar que foi carregada
    print(f"API Key carregada: ********")
else:
    print("⚠️ API Key não encontrada. Configure a variável OPENAI_API_KEY no arquivo .env")
    print("Formato do arquivo .env:")
    print("OPENAI_API_KEY=sua-chave-aqui")
    exit(1)

def test_sql_agent():
    print("Testando o SQL Agent após a correção...")
    
    try:
        # Inicializar o SQL Agent
        agent = SQLAgent()
        print("✅ SQL Agent inicializado com sucesso!")
        
        # Testar uma consulta simples
        test_query = "Quantas cargas foram registradas no ano de 2023?"
        print(f"\nExecutando consulta de teste: '{test_query}'")
        
        response = agent.process_query(test_query)
        
        print("\n--- Resultado da Consulta ---")
        print(f"Consulta: {response['query']}")
        print(f"SQL: {response['sql']}")
        print(f"Resultado: {response['result']}")
        print("-----------------------------")
        
        print("\n✅ Teste concluído com sucesso!")
        print("O SQL Agent está funcionando corretamente com o modelo deepseek.")
        
    except Exception as e:
        print(f"\n❌ Erro ao testar o SQL Agent: {e}")
        print("\nVerifique se:")
        print("1. A chave da API do OpenRouter está configurada corretamente no arquivo .env")
        print("2. O modelo deepseek está disponível e suporta ferramentas")
        print("3. A conexão com a internet está funcionando")

if __name__ == "__main__":
    test_sql_agent()
