import os
import sqlite3
from sql_agent import SQLAgent

def test_paranagua_antonina_query():
    """
    Testa a consulta sobre o volume de cargas movimentadas pelos portos de Paranaguá e Antonina em 2023,
    para verificar a discrepância entre o valor esperado (65.393.256 toneladas) e o valor retornado.
    """
    # Inicializar o agente SQL
    agent = SQLAgent()
    
    # Testar a consulta específica
    test_query = "Quantas toneladas foram movimentadas pelos portos de Paranaguá e Antonina em 2023?"
    print("\n--- Teste de Consulta para Paranaguá e Antonina em 2023 ---")
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
    
    # Verificar os códigos dos portos
    print("Verificando códigos dos portos:")
    cursor.execute("SELECT codigo, nome FROM Portos WHERE nome LIKE '%Paranagu%' OR nome LIKE '%Antonina%'")
    codigos_portos = cursor.fetchall()
    for codigo, nome in codigos_portos:
        print(f"- {nome}: {codigo}")
    
    # Se não encontrar, verificar com uma busca mais ampla
    if not codigos_portos:
        print("Buscando com critérios mais amplos:")
        cursor.execute("SELECT codigo, nome FROM Portos WHERE nome LIKE '%aranag%' OR nome LIKE '%ntonina%'")
        codigos_portos = cursor.fetchall()
        for codigo, nome in codigos_portos:
            print(f"- {nome}: {codigo}")
    
    # Consulta para verificar o volume total por porto
    print("\nVolume por porto em 2023:")
    
    # Assumindo que os códigos são BRPNG para Paranaguá e BRANT para Antonina
    # Mas vamos verificar para cada código encontrado
    for codigo, nome in codigos_portos:
        # Consulta para cargas embarcadas (exportações)
        cursor.execute(f"""
            SELECT SUM(VLPesoCargaBruta) AS Total_Embarcado
            FROM Cargas
            WHERE Sentido = 'Embarcados' AND Origem = '{codigo}' AND Ano = '2023'
        """)
        total_embarcado = cursor.fetchone()[0] or 0
        
        # Consulta para cargas desembarcadas (importações)
        cursor.execute(f"""
            SELECT SUM(VLPesoCargaBruta) AS Total_Desembarcado
            FROM Cargas
            WHERE Sentido = 'Desembarcados' AND Destino = '{codigo}' AND Ano = '2023'
        """)
        total_desembarcado = cursor.fetchone()[0] or 0
        
        total_porto = total_embarcado + total_desembarcado
        print(f"Porto {nome} ({codigo}):")
        print(f"  - Embarcado: {total_embarcado}")
        print(f"  - Desembarcado: {total_desembarcado}")
        print(f"  - Total: {total_porto}")
    
    # Consulta para o total combinado (usando os códigos encontrados)
    if codigos_portos:
        codigos = [f"'{codigo}'" for codigo, _ in codigos_portos]
        codigos_str = ", ".join(codigos)
        
        cursor.execute(f"""
            SELECT SUM(VLPesoCargaBruta) AS Total_Movimentado
            FROM Cargas
            WHERE ((Sentido = 'Embarcados' AND Origem IN ({codigos_str})) OR 
                  (Sentido = 'Desembarcados' AND Destino IN ({codigos_str}))) 
                  AND Ano = '2023'
        """)
        total_correto = cursor.fetchone()[0]
        print(f"\nTotal correto para todos os portos: {total_correto}")
    
    # Verificar se há registros que podem estar sendo contados incorretamente
    print("\nVerificando possíveis registros problemáticos:")
    
    # Verificar registros onde o porto aparece tanto na origem quanto no destino
    if codigos_portos:
        for codigo, nome in codigos_portos:
            cursor.execute(f"""
                SELECT COUNT(*) AS Registros_Duplicados, SUM(VLPesoCargaBruta) AS Volume_Duplicado
                FROM Cargas
                WHERE Origem = '{codigo}' AND Destino = '{codigo}' AND Ano = '2023'
            """)
            registros_duplicados, volume_duplicado = cursor.fetchone()
            if registros_duplicados > 0:
                print(f"Porto {nome} ({codigo}) tem {registros_duplicados} registros onde é tanto origem quanto destino, com volume de {volume_duplicado}")
    
    # Verificar se há outros registros que podem estar sendo contados incorretamente
    if codigos_portos:
        codigos = [f"'{codigo}'" for codigo, _ in codigos_portos]
        codigos_str = ", ".join(codigos)
        
        cursor.execute(f"""
            SELECT COUNT(*) AS Registros_Problematicos, SUM(VLPesoCargaBruta) AS Volume_Problematico
            FROM Cargas
            WHERE (Origem IN ({codigos_str}) OR Destino IN ({codigos_str})) 
                  AND Ano = '2023'
                  AND NOT ((Sentido = 'Embarcados' AND Origem IN ({codigos_str})) OR 
                          (Sentido = 'Desembarcados' AND Destino IN ({codigos_str})))
        """)
        registros_problematicos, volume_problematico = cursor.fetchone()
        print(f"Registros potencialmente problemáticos: {registros_problematicos}")
        print(f"Volume potencialmente problemático: {volume_problematico}")
    
    # Fechar a conexão
    conn.close()
    
    print("-----------------------------------\n")

if __name__ == "__main__":
    test_paranagua_antonina_query()
