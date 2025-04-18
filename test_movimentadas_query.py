import os
from sql_agent import SQLAgent

def test_movimentadas_query():
    """
    Testa a consulta "Quantas toneladas foram movimentadas pelo porto do itaqui em 2023?"
    para verificar se o agente interpreta corretamente como a soma de cargas embarcadas e desembarcadas.
    """
    # Inicializar o agente SQL
    agent = SQLAgent()
    
    # Testar a consulta específica
    test_query = "Quantas toneladas foram movimentadas pelo porto do itaqui em 2023?"
    print("\n--- Teste de Consulta Movimentadas ---")
    print(f"Consulta: {test_query}")
    
    # Processar a consulta
    response = agent.process_query(test_query)
    
    # Exibir o resultado
    print(f"Resultado: {response['result']}")
    print("-----------------------------------\n")

if __name__ == "__main__":
    test_movimentadas_query()
