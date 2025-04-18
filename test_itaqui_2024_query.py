import os
import sqlite3
from sql_agent import SQLAgent

def test_itaqui_2024_query():
    """
    Testa a consulta específica sobre o volume total de cargas movimentadas pelo Porto do Itaqui em 2024,
    garantindo que inclua tanto cargas embarcadas quanto desembarcadas.
    """
    # Inicializar o agente SQL
    agent = SQLAgent()
    
    # Testar a consulta específica
    test_query = "Qual o volume de cargas movimentadas pelo Porto do Itaqui em 2024?"
    print("\n--- Teste de Consulta para Porto do Itaqui em 2024 ---")
    print(f"Consulta: {test_query}")
    
    # Processar a consulta
    response = agent.process_query(test_query)
    
    # Exibir o resultado
    print(f"Resultado: {response['result']}")
    
    # Testar consultas separadas para verificar os componentes
    print("\n--- Verificando componentes da consulta ---")
    
    # Consulta para cargas embarcadas (exportações)
    embarcadas_query = "Qual o volume de cargas embarcadas pelo Porto do Itaqui em 2024?"
    embarcadas_response = agent.process_query(embarcadas_query)
    print(f"Volume embarcado: {embarcadas_response['result']}")
    
    # Consulta para cargas desembarcadas (importações)
    desembarcadas_query = "Qual o volume de cargas desembarcadas no Porto do Itaqui em 2024?"
    desembarcadas_response = agent.process_query(desembarcadas_query)
    print(f"Volume desembarcado: {desembarcadas_response['result']}")
    
    # Verificar diretamente com SQL para identificar o problema
    print("\n--- Verificação direta com SQL ---")
    
    # Conectar ao banco de dados
    conn = sqlite3.connect(agent.db_path)
    cursor = conn.cursor()
    
    # Consulta para cargas embarcadas (exportações)
    cursor.execute("""
        SELECT SUM(VLPesoCargaBruta) AS Total_Embarcado
        FROM Cargas
        WHERE Sentido = 'Embarcados' AND Origem = 'BRIQI' AND Ano = '2024'
    """)
    total_embarcado = cursor.fetchone()[0]
    print(f"SQL direto - Volume embarcado: {total_embarcado}")
    
    # Consulta para cargas desembarcadas (importações)
    cursor.execute("""
        SELECT SUM(VLPesoCargaBruta) AS Total_Desembarcado
        FROM Cargas
        WHERE Sentido = 'Desembarcados' AND Destino = 'BRIQI' AND Ano = '2024'
    """)
    total_desembarcado = cursor.fetchone()[0]
    print(f"SQL direto - Volume desembarcado: {total_desembarcado}")
    
    # Consulta para o total (embarcado + desembarcado)
    cursor.execute("""
        SELECT SUM(VLPesoCargaBruta) AS Total_Movimentado
        FROM Cargas
        WHERE ((Sentido = 'Embarcados' AND Origem = 'BRIQI') OR 
               (Sentido = 'Desembarcados' AND Destino = 'BRIQI')) 
              AND Ano = '2024'
    """)
    total_correto = cursor.fetchone()[0]
    print(f"SQL direto - Volume total correto: {total_correto}")
    
    # Consulta para identificar o problema (o que está sendo contado a mais)
    cursor.execute("""
        SELECT SUM(VLPesoCargaBruta) AS Total_Geral
        FROM Cargas
        WHERE (Origem = 'BRIQI' OR Destino = 'BRIQI') AND Ano = '2024'
    """)
    total_geral = cursor.fetchone()[0]
    print(f"SQL direto - Volume total sem filtro de sentido: {total_geral}")
    
    # Verificar registros que podem estar sendo contados incorretamente
    cursor.execute("""
        SELECT COUNT(*) AS Registros_Problematicos, SUM(VLPesoCargaBruta) AS Volume_Problematico
        FROM Cargas
        WHERE (Origem = 'BRIQI' OR Destino = 'BRIQI') 
              AND Ano = '2024'
              AND NOT ((Sentido = 'Embarcados' AND Origem = 'BRIQI') OR 
                       (Sentido = 'Desembarcados' AND Destino = 'BRIQI'))
    """)
    registros_problematicos, volume_problematico = cursor.fetchone()
    print(f"Registros potencialmente problemáticos: {registros_problematicos}")
    print(f"Volume potencialmente problemático: {volume_problematico}")
    
    # Fechar a conexão
    conn.close()
    
    print("-----------------------------------\n")

if __name__ == "__main__":
    test_itaqui_2024_query()
