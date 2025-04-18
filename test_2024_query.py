import os
from sql_agent import SQLAgent

def test_2024_query():
    # Inicializar o agente SQL
    agent = SQLAgent()
    
    # Testar a consulta específica mencionada no exemplo para 2024
    test_query = "Quantas toneladas foram embarcadas pelo Porto do Itaqui em 2024?"
    print("\n--- Teste de Consulta para 2024 ---")
    print(f"Consulta: {test_query}")
    
    # Processar a consulta
    response = agent.process_query(test_query)
    
    # Exibir o resultado
    print(f"Resultado: {response['result']}")
    print("-----------------------------------\n")

if __name__ == "__main__":
    test_2024_query()
