import streamlit as st
# from database_tools import DatabaseTools # No longer needed directly here
from sql_agent import SQLAgent
import pandas as pd
import os

from dotenv import load_dotenv
load_dotenv()
 
# Configuração da página
st.set_page_config(
    page_title="Agente SQL em Linguagem Natural",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# DB_PATH is now handled within SQLAgent initialization

# DatabaseTools is no longer initialized directly here
# @st.cache_resource
# def get_db_tools():
#     # Find DB path dynamically or rely on SQLAgent's logic
#     # This function might be removed or adapted if schema display is needed differently
#     pass 

# Inicializar o agente SQL (now finds DB path itself)
@st.cache_resource
def get_sql_agent():
    # db_tools = get_db_tools() # No longer pass db_tools
    return SQLAgent() # Initialize without arguments

# Função para exibir o esquema do banco de dados (Commented out as DatabaseTools is removed)
# def show_database_schema():
#     # This needs reimplementation if schema display is desired without DatabaseTools
#     st.warning("Funcionalidade de exibição de esquema temporariamente desativada.")
#     # db_tools = get_db_tools() 
#     # ... (rest of the old code)

# Função para processar consultas
def process_query(query):
    agent = get_sql_agent() # Agent is already cached
    result = agent.process_query(query)
    return result

# Função para exibir o histórico de consultas
def show_history():
    agent = get_sql_agent() # Agent is already cached
    memory = agent.get_memory()
    
    if not memory:
        st.info("Nenhuma consulta realizada ainda.")
        return
    
    for i, item in enumerate(memory):
        with st.expander(f"Consulta {i+1}: {item['query']}"):
            # Display SQL placeholder and result (now likely a string)
            st.markdown(f"**SQL Gerado (interno ao agente):** `{item['sql']}`")
            st.markdown("**Resultado:**")
            # Display result as text/markdown, as it's not guaranteed to be a DataFrame
            st.write(item['result']) 

# Interface principal
def main():
    st.title("🤖 Agente SQL em Linguagem Natural")
    st.markdown("""
    Este aplicativo permite que você faça consultas em linguagem natural ao banco de dados de cargas.
    O agente de IA traduzirá sua pergunta para SQL e retornará os resultados.
    """)
    
    # Barra lateral
    st.sidebar.title("Navegação")
    # Temporarily remove "Esquema do Banco" option
    page = st.sidebar.radio("Ir para:", ["Consulta", "Histórico"]) 
    
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
                st.subheader("Consulta SQL (Gerada pelo Agente):")
                # Display the placeholder SQL info
                st.markdown(f"`{result['sql']}`") 
                
                # Exibir os resultados (now likely a string)
                st.subheader("Resultados:")
                # Display the agent's text output
                st.write(result['result']) 
            else:
                st.warning("Por favor, digite uma pergunta.")
    
    # Página de esquema do banco (Commented out)
    # elif page == "Esquema do Banco":
    #     st.header("Esquema do Banco de Dados")
    #     show_database_schema() # Function is commented out
    
    # Página de histórico
    elif page == "Histórico":
        st.header("Histórico de Consultas")
        show_history()

if __name__ == "__main__":
    main()
