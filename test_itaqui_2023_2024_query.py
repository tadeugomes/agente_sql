import os
import sqlite3
from sql_agent import SQLAgent

def test_itaqui_2023_2024_query():
    """
    Testa a consulta sobre o volume de cargas movimentadas pelo Porto do Itaqui em 2023 e 2024,
    mostrando os resultados para cada ano separadamente.
    """
    # Inicializar o agente SQL
    agent = SQLAgent()
    
    # Testar a consulta para 2023
    query_2023 = "Qual o volume de cargas movimentadas pelo Porto do Itaqui em 2023?"
    print("\n--- Volume de Cargas Movimentadas pelo Porto do Itaqui em 2023 ---")
    print(f"Consulta: {query_2023}")
    
    # Processar a consulta
    response_2023 = agent.process_query(query_2023)
    
    # Exibir o resultado
    print(f"Resultado: {response_2023['result']}")
    
    # Testar a consulta para 2024
    query_2024 = "Qual o volume de cargas movimentadas pelo Porto do Itaqui em 2024?"
    print("\n--- Volume de Cargas Movimentadas pelo Porto do Itaqui em 2024 ---")
    print(f"Consulta: {query_2024}")
    
    # Processar a consulta
    response_2024 = agent.process_query(query_2024)
    
    # Exibir o resultado
    print(f"Resultado: {response_2024['result']}")
    
    # Verificar diretamente com SQL para confirmar os resultados
    print("\n--- Verificação direta com SQL ---")
    
    # Conectar ao banco de dados
    conn = sqlite3.connect(agent.db_path)
    cursor = conn.cursor()
    
    # Consulta para 2023
    cursor.execute("""
        SELECT SUM(VLPesoCargaBruta) AS Total_Movimentado_2023
        FROM Cargas
        WHERE ((Sentido = 'Embarcados' AND Origem = 'BRIQI') OR 
               (Sentido = 'Desembarcados' AND Destino = 'BRIQI')) 
              AND Ano = '2023'
    """)
    total_2023 = cursor.fetchone()[0]
    print(f"SQL direto - Volume total em 2023: {total_2023}")
    
    # Consulta para 2024
    cursor.execute("""
        SELECT SUM(VLPesoCargaBruta) AS Total_Movimentado_2024
        FROM Cargas
        WHERE ((Sentido = 'Embarcados' AND Origem = 'BRIQI') OR 
               (Sentido = 'Desembarcados' AND Destino = 'BRIQI')) 
              AND Ano = '2024'
    """)
    total_2024 = cursor.fetchone()[0]
    print(f"SQL direto - Volume total em 2024: {total_2024}")
    
    # Consulta para ambos os anos juntos
    cursor.execute("""
        SELECT Ano, SUM(VLPesoCargaBruta) AS Total_Movimentado
        FROM Cargas
        WHERE ((Sentido = 'Embarcados' AND Origem = 'BRIQI') OR 
               (Sentido = 'Desembarcados' AND Destino = 'BRIQI')) 
              AND Ano IN ('2023', '2024')
        GROUP BY Ano
        ORDER BY Ano
    """)
    resultados = cursor.fetchall()
    print("\nResultados por ano:")
    for ano, total in resultados:
        print(f"Ano {ano}: {total} toneladas")
    
    # Fechar a conexão
    conn.close()
    
    print("-----------------------------------\n")

if __name__ == "__main__":
    test_itaqui_2023_2024_query()
