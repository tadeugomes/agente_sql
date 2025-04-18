import sqlite3
import pandas as pd

class DatabaseTools:
    def __init__(self, db_path):
        """
        Inicializa as ferramentas de interação com o banco de dados.
        
        Args:
            db_path (str): Caminho para o arquivo do banco de dados SQLite.
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
    
    def connect(self):
        """
        Estabelece conexão com o banco de dados.
        
        Returns:
            bool: True se a conexão foi estabelecida com sucesso, False caso contrário.
        """
        try:
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            return True
        except Exception as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return False
    
    def disconnect(self):
        """
        Fecha a conexão com o banco de dados.
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None
    
    def list_tables(self):
        """
        Lista todas as tabelas disponíveis no banco de dados.
        
        Returns:
            list: Lista de nomes das tabelas.
        """
        if not self.connect():
            return []
        
        try:
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [table[0] for table in self.cursor.fetchall()]
            return tables
        except Exception as e:
            print(f"Erro ao listar tabelas: {e}")
            return []
        finally:
            self.disconnect()
    
    def describe_table(self, table_name):
        """
        Descreve a estrutura de uma tabela (colunas e tipos de dados).
        
        Args:
            table_name (str): Nome da tabela a ser descrita.
            
        Returns:
            pd.DataFrame: DataFrame com informações sobre as colunas da tabela.
        """
        if not self.connect():
            return pd.DataFrame()
        
        try:
            # Obter informações sobre as colunas
            self.cursor.execute(f"PRAGMA table_info({table_name});")
            columns_info = self.cursor.fetchall()
            
            # Criar DataFrame com as informações
            columns_df = pd.DataFrame(columns_info, 
                                     columns=['cid', 'name', 'type', 'notnull', 'default_value', 'pk'])
            
            # Selecionar apenas as colunas relevantes
            result_df = columns_df[['name', 'type', 'pk']]
            result_df.columns = ['Coluna', 'Tipo', 'Chave Primária']
            result_df['Chave Primária'] = result_df['Chave Primária'].apply(lambda x: 'Sim' if x == 1 else 'Não')
            
            return result_df
        except Exception as e:
            print(f"Erro ao descrever tabela {table_name}: {e}")
            return pd.DataFrame()
        finally:
            self.disconnect()
    
    def sample_table(self, table_name, limit=10):
        """
        Amostra um número limitado de linhas de uma tabela.
        
        Args:
            table_name (str): Nome da tabela a ser amostrada.
            limit (int): Número máximo de linhas a serem retornadas.
            
        Returns:
            pd.DataFrame: DataFrame com as linhas amostradas.
        """
        if not self.connect():
            return pd.DataFrame()
        
        try:
            query = f"SELECT * FROM {table_name} LIMIT {limit};"
            df = pd.read_sql_query(query, self.conn)
            return df
        except Exception as e:
            print(f"Erro ao amostrar tabela {table_name}: {e}")
            return pd.DataFrame()
        finally:
            self.disconnect()
    
    def execute_query(self, query):
        """
        Executa uma consulta SQL diretamente.
        
        Args:
            query (str): Consulta SQL a ser executada.
            
        Returns:
            pd.DataFrame: DataFrame com os resultados da consulta.
        """
        if not self.connect():
            return pd.DataFrame()
        
        try:
            # Verificar se a consulta é segura (não permite modificações no banco)
            query_lower = query.lower().strip()
            if query_lower.startswith(('insert', 'update', 'delete', 'drop', 'alter', 'create')):
                return pd.DataFrame({'error': ['Consultas de modificação não são permitidas por segurança.']})
            
            df = pd.read_sql_query(query, self.conn)
            return df
        except Exception as e:
            print(f"Erro ao executar consulta: {e}")
            return pd.DataFrame({'error': [str(e)]})
        finally:
            self.disconnect()
