import os
import sqlite3
import json
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain.agents.agent_types import AgentType
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
import streamlit as st
from openai import OpenAI

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

def get_openai_api_key():
    """
    Get the OpenAI API key from Streamlit secrets
    """
    try:
        api_key = st.secrets["OPENAI_API_KEY"]
        # Debug: verificar se a chave está presente (apenas os primeiros caracteres)
        st.write(f"API Key encontrada: {api_key[:10]}...")
        return api_key
    except Exception as e:
        st.error(f"Erro ao obter a chave da API: {str(e)}")
        raise

class SQLAgent:
    def __init__(self, db_path=None):
        """
        Initialize the SQL Agent with configuration
        """
        try:
            self.api_key = get_openai_api_key()
            
            # Inicializar cliente OpenAI
            self.client = OpenAI(api_key=self.api_key)
            
            # Se não foi fornecido um caminho para o banco, usar o padrão
            if not db_path:
                db_path = os.path.join(os.path.dirname(__file__), 'cargas.db')
            
            # Verificar se o arquivo do banco existe
            if not os.path.exists(db_path):
                raise FileNotFoundError(f"Banco de dados não encontrado em: {db_path}")
            
            # Inicializar o SQLDatabase do LangChain
            self.db = SQLDatabase.from_uri(f"sqlite:///{db_path}")
            
            # Configurar o modelo de linguagem
            self.llm = ChatOpenAI(
                temperature=0,
                model="gpt-4-1106-preview",
                api_key=self.api_key
            )
            
            # Criar o agente SQL
            self.agent_executor = create_sql_agent(
                llm=self.llm,
                db=self.db,
                agent_type=AgentType.OPENAI_FUNCTIONS,
                verbose=True
            )
        except Exception as e:
            st.error(f"Erro na inicialização do SQLAgent: {str(e)}")
            raise
    
    def process_query(self, query):
        """
        Process a natural language query and return the results
        """
        try:
            # Executar a consulta através do agente
            result = self.agent_executor.invoke({"input": query})
            
            # Extrair SQL da resposta (se disponível)
            sql = "Query SQL não disponível"
            if "sql_cmd" in result.get("intermediate_steps", []):
                sql = result["intermediate_steps"]["sql_cmd"]
            
            return {
                "query": query,
                "sql": sql,
                "result": result["output"]
            }
            
        except Exception as e:
            return {
                "query": query,
                "sql": "Error during agent execution",
                "result": f"Erro: {str(e)}"
            }

if __name__ == '__main__':
    try:
        agent = SQLAgent()
        test_query = "Quantas cargas foram registradas no ano de 2023?"
        result = agent.process_query(test_query)
        print("\nResultado do teste:")
        print(f"Consulta: {result['query']}")
        print(f"SQL: {result['sql']}")
        print(f"Resultado: {result['result']}")
    except Exception as e:
        print(f"Erro ao executar o teste: {e}")
