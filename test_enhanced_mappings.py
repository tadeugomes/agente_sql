import os
from sql_agent import SQLAgent

def test_enhanced_mappings():
    """
    Testa as consultas com mapeamentos semânticos aprimorados.
    """
    # Inicializar o agente SQL
    agent = SQLAgent()
    
    # Lista de consultas para testar os diferentes mapeamentos semânticos
    test_queries = [
        # Teste de mercadorias
        "Quantas toneladas de animais vivos foram embarcadas em 2023?",
        
        # Teste de países
        "Qual o volume de carga exportada do Brasil para a China em 2023?",
        
        # Teste de tipo de navegação
        "Quantas cargas de cabotagem passaram pelo Porto de Santos em 2023?",
        
        # Teste de natureza da carga
        "Qual o volume de granéis líquidos movimentados em 2023?",
        
        # Teste de TEUs
        "Quantos TEUs foram movimentados pelo Porto de Santos em 2023?",
        
        # Teste de comparação
        "Quais portos movimentaram mais de 500 mil toneladas em 2023?",
        
        # Teste de agregação
        "Qual a média mensal de cargas embarcadas em 2023?",
    ]
    
    # Processar cada consulta e exibir os resultados
    for i, query in enumerate(test_queries):
        print(f"\n--- Teste {i+1}: {query} ---")
        
        # Processar a consulta
        response = agent.process_query(query)
        
        # Exibir o resultado
        print(f"Resultado: {response['result']}")
        print("-----------------------------------")

if __name__ == "__main__":
    test_enhanced_mappings()
