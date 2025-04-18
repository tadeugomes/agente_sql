import os
from sql_agent import SQLAgent

def test_contextual_query():
    # Inicializar o agente SQL
    agent = SQLAgent()
    
    # Testar a consulta específica mencionada no exemplo
    test_query = "Quantas toneladas foram embarcadas pelo Porto do Itaqui em 2023?"
    print("\n--- Teste de Consulta Contextual ---")
    print(f"Consulta: {test_query}")
    
    # Processar a consulta
    response = agent.process_query(test_query)
    
    # Exibir o resultado
    print(f"Resultado: {response['result']}")
    print("-----------------------------------\n")
    
    # Testar outra consulta contextual
    test_query_2 = "Qual o total de toneladas desembarcadas em Santos em 2023?"
    print("\n--- Teste de Consulta Contextual 2 ---")
    print(f"Consulta: {test_query_2}")
    
    # Processar a consulta
    response_2 = agent.process_query(test_query_2)
    
    # Exibir o resultado
    print(f"Resultado: {response_2['result']}")
    print("-----------------------------------\n")

if __name__ == "__main__":
    test_contextual_query()
