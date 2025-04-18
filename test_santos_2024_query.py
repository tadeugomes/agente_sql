import os
import sqlite3
from sql_agent import SQLAgent

def test_santos_2024_query():
    """
    Testa a consulta sobre o volume de cargas embarcadas pelo Porto de Santos em 2024,
    para verificar a discrepância entre o valor esperado (131,3 milhões de toneladas) e o valor retornado.
    """
    # Inicializar o agente SQL
    agent = SQLAgent()
    
    # Testar a consulta específica
    test_query = "Quantas toneladas foram embarcadas pelo porto de Santos em 2024?"
    print("\n--- Teste de Consulta para Embarques em Santos em 2024 ---")
    print(f"Consulta: {test_query}")
    
    # Processar a consulta
    response = agent.process_query(test_query)
    
    # Exibir o resultado
    print(f"Resultado: {response['result']}")
    
    # Verificar diretamente com SQL para confirmar os resultados
    print("\n--- Verificação direta com SQL ---")
    
    # Conectar ao banco de dados
    conn = sqlite3.connect(agent.db_path)
    cursor = conn.cursor()
    
    # Consulta para cargas embarcadas pelo Porto de Santos (BRSSZ) em 2024
    cursor.execute("""
        SELECT SUM(VLPesoCargaBruta) AS Total_Embarcado_Santos
        FROM Cargas
        WHERE Sentido = 'Embarcados' AND Origem = 'BRSSZ' AND Ano = '2024'
    """)
    total_santos = cursor.fetchone()[0] or 0
    print(f"Porto Santos (BRSSZ) em 2024: {total_santos} toneladas")
    
    # Consulta para cargas embarcadas pelo terminal DP World Santos (BRSP008) em 2024
    cursor.execute("""
        SELECT SUM(VLPesoCargaBruta) AS Total_Embarcado_DPWorld
        FROM Cargas
        WHERE Sentido = 'Embarcados' AND Origem = 'BRSP008' AND Ano = '2024'
    """)
    total_dpworld = cursor.fetchone()[0] or 0
    print(f"DP World Santos (BRSP008) em 2024: {total_dpworld} toneladas")
    
    # Consulta para o total combinado
    cursor.execute("""
        SELECT SUM(VLPesoCargaBruta) AS Total_Embarcado_Combinado
        FROM Cargas
        WHERE Sentido = 'Embarcados' AND Origem IN ('BRSSZ', 'BRSP008') AND Ano = '2024'
    """)
    total_combinado = cursor.fetchone()[0] or 0
    print(f"Total combinado em 2024: {total_combinado} toneladas")
    
    # Verificar se há outros terminais relacionados a Santos
    cursor.execute("""
        SELECT Origem, Origem_Nome, COUNT(*) AS Registros, SUM(VLPesoCargaBruta) AS Volume
        FROM Cargas
        WHERE (Origem_Nome LIKE '%Santos%' OR Origem_Nome LIKE '%Terminal%Santos%' OR Origem_Nome LIKE '%Santos%Terminal%')
        AND Origem NOT IN ('BRSSZ', 'BRSP008')
        AND Sentido = 'Embarcados'
        AND Ano = '2024'
        GROUP BY Origem, Origem_Nome
        ORDER BY Volume DESC
    """)
    outros_terminais = cursor.fetchall()
    if outros_terminais:
        print("\nOutros possíveis terminais de Santos em 2024:")
        total_outros = 0
        for codigo, nome, registros, volume in outros_terminais:
            print(f"- {nome} ({codigo}): {registros} registros, {volume} toneladas")
            total_outros += volume
        
        print(f"\nVolume total de outros terminais: {total_outros} toneladas")
        print(f"Volume total incluindo todos os terminais: {total_combinado + total_outros} toneladas")
    
    # Fechar a conexão
    conn.close()
    
    print("-----------------------------------\n")

if __name__ == "__main__":
    test_santos_2024_query()
