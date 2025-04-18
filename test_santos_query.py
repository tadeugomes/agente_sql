import os
import sqlite3
from sql_agent import SQLAgent

def test_santos_query():
    """
    Testa a consulta sobre o volume de cargas embarcadas pelo Porto de Santos,
    para verificar a discrepância entre o valor esperado (131,3 milhões de toneladas) e o valor retornado.
    """
    # Inicializar o agente SQL
    agent = SQLAgent()
    
    # Testar a consulta específica
    test_query = "Quantas toneladas foram embarcadas pelo porto de Santos?"
    print("\n--- Teste de Consulta para Embarques em Santos ---")
    print(f"Consulta: {test_query}")
    
    # Processar a consulta
    response = agent.process_query(test_query)
    
    # Exibir o resultado
    print(f"Resultado: {response['result']}")
    
    # Verificar diretamente com SQL para identificar o problema
    print("\n--- Verificação direta com SQL ---")
    
    # Conectar ao banco de dados
    conn = sqlite3.connect(agent.db_path)
    cursor = conn.cursor()
    
    # Verificar os códigos do porto
    print("Verificando códigos do porto:")
    cursor.execute("SELECT codigo, nome FROM Portos WHERE nome LIKE '%Santos%'")
    codigos_porto = cursor.fetchall()
    for codigo, nome in codigos_porto:
        print(f"- {nome}: {codigo}")
    
    # Se não encontrar, verificar com uma busca mais ampla
    if not codigos_porto:
        print("Buscando com critérios mais amplos:")
        cursor.execute("SELECT codigo, nome FROM Portos WHERE nome LIKE '%antos%'")
        codigos_porto = cursor.fetchall()
        for codigo, nome in codigos_porto:
            print(f"- {nome}: {codigo}")
    
    # Consulta para verificar o volume total de embarques
    print("\nVolume de embarques por código de porto:")
    
    # Assumindo que o código é BRSSZ para Santos
    # Mas vamos verificar para cada código encontrado
    for codigo, nome in codigos_porto:
        # Consulta para cargas embarcadas (exportações)
        cursor.execute(f"""
            SELECT SUM(VLPesoCargaBruta) AS Total_Embarcado
            FROM Cargas
            WHERE Sentido = 'Embarcados' AND Origem = '{codigo}'
        """)
        total_embarcado = cursor.fetchone()[0] or 0
        print(f"Porto {nome} ({codigo}):")
        print(f"  - Total embarcado (todos os anos): {total_embarcado}")
        
        # Consulta por ano
        cursor.execute(f"""
            SELECT Ano, SUM(VLPesoCargaBruta) AS Total_Embarcado
            FROM Cargas
            WHERE Sentido = 'Embarcados' AND Origem = '{codigo}'
            GROUP BY Ano
            ORDER BY Ano
        """)
        resultados_por_ano = cursor.fetchall()
        print("  - Embarques por ano:")
        for ano, total in resultados_por_ano:
            print(f"    {ano}: {total}")
    
    # Verificar se há registros que podem estar sendo contados incorretamente
    print("\nVerificando possíveis registros problemáticos:")
    
    # Verificar registros com Santos no nome do porto de origem, mas não no código
    if codigos_porto:
        codigos = [f"'{codigo}'" for codigo, _ in codigos_porto]
        codigos_str = ", ".join(codigos)
        
        cursor.execute(f"""
            SELECT COUNT(*) AS Registros_Santos_Nome, SUM(VLPesoCargaBruta) AS Volume_Santos_Nome
            FROM Cargas
            WHERE Origem_Nome LIKE '%Santos%' AND Origem NOT IN ({codigos_str})
            AND Sentido = 'Embarcados'
        """)
        registros_santos_nome, volume_santos_nome = cursor.fetchone()
        print(f"Registros com 'Santos' no nome do porto de origem, mas não no código: {registros_santos_nome}")
        print(f"Volume desses registros: {volume_santos_nome}")
        
        # Verificar registros com outros códigos que podem ser terminais de Santos
        cursor.execute("""
            SELECT Origem, Origem_Nome, COUNT(*) AS Registros, SUM(VLPesoCargaBruta) AS Volume
            FROM Cargas
            WHERE (Origem_Nome LIKE '%Santos%' OR Origem_Nome LIKE '%Terminal%Santos%' OR Origem_Nome LIKE '%Santos%Terminal%')
            AND Sentido = 'Embarcados'
            GROUP BY Origem, Origem_Nome
            ORDER BY Volume DESC
        """)
        terminais_santos = cursor.fetchall()
        print("\nPossíveis terminais de Santos:")
        total_volume_terminais = 0
        for codigo, nome, registros, volume in terminais_santos:
            print(f"- {nome} ({codigo}): {registros} registros, {volume} toneladas")
            total_volume_terminais += volume
        
        print(f"\nVolume total de todos os possíveis terminais de Santos: {total_volume_terminais}")
    
    # Fechar a conexão
    conn.close()
    
    print("-----------------------------------\n")

if __name__ == "__main__":
    test_santos_query()
