import os
import sys
from database_tools import DatabaseTools

# Configurar o caminho do banco de dados dinamicamente
DB_PATH = os.path.join(os.getcwd(), 'sql_agent', 'cargas.db')

# Verificar se o arquivo do banco de dados existe
if not os.path.exists(DB_PATH):
    print(f"❌ Erro: O arquivo do banco de dados não foi encontrado no caminho: {DB_PATH}")
    sys.exit(1)

# Inicializar as ferramentas de banco de dados
db_tools = DatabaseTools(DB_PATH)

def test_database_tools():
    """Testa as ferramentas de interação com o banco de dados"""
    print("=== Testando ferramentas de banco de dados ===")
    
    # Testar listagem de tabelas
    print("\n1. Testando listagem de tabelas:")
    tables = db_tools.list_tables()
    print(f"Tabelas encontradas: {tables}")
    assert len(tables) > 0, "Erro: Nenhuma tabela encontrada"
    
    # Testar descrição de tabela
    print("\n2. Testando descrição de tabela:")
    table_to_test = "Cargas"
    structure = db_tools.describe_table(table_to_test)
    print(f"Estrutura da tabela {table_to_test}:")
    print(structure)
    assert not structure.empty, f"Erro: Não foi possível descrever a tabela {table_to_test}"
    
    # Testar amostragem de tabela
    print("\n3. Testando amostragem de tabela:")
    sample = db_tools.sample_table(table_to_test, 3)
    print(f"Amostra da tabela {table_to_test}:")
    print(sample)
    assert not sample.empty, f"Erro: Não foi possível amostrar a tabela {table_to_test}"
    
    # Testar execução de consulta
    print("\n4. Testando execução de consulta:")
    query = "SELECT COUNT(*) as total FROM Cargas;"
    result = db_tools.execute_query(query)
    print(f"Resultado da consulta: {query}")
    print(result)
    assert not result.empty, "Erro: Não foi possível executar a consulta"
    
    print("\n✅ Todos os testes de ferramentas de banco de dados passaram com sucesso!")

def test_queries():
    """Testa consultas SQL diretas para validar o banco de dados"""
    print("\n=== Testando consultas SQL ===")
    
    # Teste 1: Contar registros por ano
    print("\n1. Contagem de registros por ano:")
    query = "SELECT Ano, COUNT(*) as total FROM Cargas GROUP BY Ano ORDER BY Ano;"
    result = db_tools.execute_query(query)
    print(result)
    assert not result.empty, "Erro: Consulta de contagem por ano falhou"
    
    # Teste 2: Top 5 mercadorias mais frequentes
    print("\n2. Top 5 mercadorias mais frequentes:")
    query = """
    SELECT c.CDMercadoria, m.descricao, COUNT(*) as total 
    FROM Cargas c
    JOIN CDMercadoria m ON c.CDMercadoria = m.codigo
    GROUP BY c.CDMercadoria, m.descricao
    ORDER BY total DESC
    LIMIT 5;
    """
    result = db_tools.execute_query(query)
    print(result)
    assert not result.empty, "Erro: Consulta de top mercadorias falhou"
    
    # Teste 3: Peso médio de carga por tipo de navegação
    print("\n3. Peso médio de carga por tipo de navegação:")
    query = """
    SELECT c.TipoNavegacao_Codigo, t.descricao, AVG(c.VLPesoCargaBruta) as peso_medio
    FROM Cargas c
    LEFT JOIN TipoNavegacao t ON c.TipoNavegacao_Codigo = t.codigo
    GROUP BY c.TipoNavegacao_Codigo, t.descricao
    ORDER BY peso_medio DESC;
    """
    result = db_tools.execute_query(query)
    print(result)
    assert not result.empty, "Erro: Consulta de peso médio falhou"
    
    print("\n✅ Todos os testes de consultas SQL passaram com sucesso!")

if __name__ == "__main__":
    try:
        # Testar ferramentas de banco de dados
        test_database_tools()
        
        # Testar consultas SQL
        test_queries()
        
        print("\n🎉 Todos os testes foram concluídos com sucesso!")
        
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        sys.exit(1)
