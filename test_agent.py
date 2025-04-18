import os
import sys
from database_tools import DatabaseTools
from sql_agent import SQLAgent

# Configurar o caminho do banco de dados
DB_PATH = os.path.join(os.getcwd(),'cargas.db')

# Inicializar as ferramentas de banco de dados
db_tools = DatabaseTools(DB_PATH)

def test_sql_agent():
    """Testa o agente SQL com consultas em linguagem natural"""
    print("=== Testando o agente SQL com consultas em linguagem natural ===")
    
    # Inicializar o agente SQL
    try:
        agent = SQLAgent(DB_PATH)
        print("✅ Agente SQL inicializado com sucesso!")
    except Exception as e:
        print(f"❌ Erro ao inicializar o agente SQL: {e}")
        return False
    
    # Lista de consultas de teste em linguagem natural
    test_queries = [
        "Quantas cargas foram registradas em 2023?",
        "Quais são as 5 mercadorias mais frequentes?",
        "Qual é o peso médio das cargas por tipo de navegação?"
    ]
    
    # Testar cada consulta
    for i, query in enumerate(test_queries):
        print(f"\n{i+1}. Testando consulta: '{query}'")
        try:
            print("Processando consulta...")
            result = agent.process_query(query)
            
            print(f"SQL gerado: {result['sql']}")
            print("Resultado:")
            print(result['result'])
            
            assert result['result'], "Resultado vazio"
            print(f"✅ Consulta {i+1} processada com sucesso!")
        except Exception as e:
            print(f"❌ Erro ao processar consulta {i+1}: {e}")
            return False
    
    print("\n✅ Todos os testes do agente SQL passaram com sucesso!")
    return True

def test_streamlit_app():
    """Verifica se a aplicação Streamlit está pronta para execução"""
    print("\n=== Verificando a aplicação Streamlit ===")
    
    app_path = os.path.join(os.getcwd(), 'app.py')
    
    if not os.path.exists(app_path):
        print(f"❌ Arquivo da aplicação não encontrado: {app_path}")
        return False
    
    print(f"✅ Arquivo da aplicação encontrado: {app_path}")
    print("✅ A aplicação Streamlit está pronta para execução!")
    return True

if __name__ == "__main__":
    try:
        # Testar o agente SQL
        agent_success = test_sql_agent()
        
        # Testar a aplicação Streamlit
        app_success = test_streamlit_app()
        
        if agent_success and app_success:
            print("\n🎉 Todos os testes foram concluídos com sucesso!")
            print("\nPara executar a aplicação, use o comando:")
            print(f"streamlit run {os.path.join(os.getcwd(), 'app.py')}")
        else:
            print("\n❌ Alguns testes falharam. Verifique os erros acima.")
            sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Erro durante os testes: {e}")
        sys.exit(1)
