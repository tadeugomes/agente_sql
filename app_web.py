import streamlit as st
from database_tools import DatabaseTools
from sql_agent import SQLAgent
import pandas as pd
import os

# Configuração da página
st.set_page_config(
    page_title="Agente SQL em Linguagem Natural",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Caminho para o banco de dados
DB_PATH = './cargas.db'

# Inicializar as ferramentas de banco de dados
@st.cache_resource
def get_db_tools():
    return DatabaseTools(DB_PATH)

# Inicializar o agente SQL
@st.cache_resource
def get_sql_agent():
    db_tools = get_db_tools()
    return SQLAgent(db_tools)

# Função para exibir o esquema do banco de dados
def show_database_schema():
    db_tools = get_db_tools()
    
    # Obter lista de tabelas
    tables = db_tools.list_tables()
    
    # Exibir informações de cada tabela
    for table in tables:
        with st.expander(f"Tabela: {table}"):
            # Exibir estrutura da tabela
            st.subheader("Estrutura")
            structure = db_tools.describe_table(table)
            st.dataframe(structure)
            
            # Exibir amostra de dados
            st.subheader("Amostra de Dados")
            sample = db_tools.sample_table(table, 5)
            st.dataframe(sample)

# Função para processar consultas
def process_query(query):
    agent = get_sql_agent()
    result = agent.process_query(query)
    return result

# Função para exibir o histórico de consultas
def show_history():
    agent = get_sql_agent()
    memory = agent.get_memory()
    
    if not memory:
        st.info("Nenhuma consulta realizada ainda.")
        return
    
    for i, item in enumerate(memory):
        with st.expander(f"Consulta {i+1}: {item['query']}"):
            st.code(item['sql'], language="sql")
            st.dataframe(item['result'])

# Interface principal
def main():
    st.title("🤖 Agente SQL em Linguagem Natural")
    st.markdown("""
    Este aplicativo permite que você faça consultas em linguagem natural ao banco de dados de cargas.
    O agente de IA traduzirá sua pergunta para SQL e retornará os resultados.
    """)
    
    # Barra lateral
    st.sidebar.title("Navegação")
    page = st.sidebar.radio("Ir para:", ["Consulta", "Esquema do Banco", "Histórico"])
    
    # Página de consulta
    if page == "Consulta":
        st.header("Faça sua pergunta")
        
        # Campo de entrada para a consulta
        query = st.text_area("Digite sua pergunta em linguagem natural:", 
                            placeholder="Exemplo: Quantas cargas foram registradas em 2023?",
                            height=100)
        
        # Botão para processar a consulta
        if st.button("Processar Consulta"):
            if query:
                with st.spinner("Processando sua consulta..."):
                    result = process_query(query)
                
                # Exibir a consulta SQL gerada
                st.subheader("Consulta SQL gerada:")
                st.code(result['sql'], language="sql")
                
                # Exibir os resultados
                st.subheader("Resultados:")
                if 'error' in result['result'].columns:
                    st.error(result['result']['error'][0])
                else:
                    st.dataframe(result['result'])
            else:
                st.warning("Por favor, digite uma pergunta.")
    
    # Página de esquema do banco
    elif page == "Esquema do Banco":
        st.header("Esquema do Banco de Dados")
        show_database_schema()
    
    # Página de histórico
    elif page == "Histórico":
        st.header("Histórico de Consultas")
        show_history()

if __name__ == "__main__":
    main()
