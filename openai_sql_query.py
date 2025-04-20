"""
Este script implementa uma abordagem mais simples para consultas SQL em linguagem natural,
usando a API do OpenAI diretamente em vez de OpenRouter.
"""

import os
import sqlite3
from dotenv import load_dotenv
from openai import OpenAI
from langchain_community.utilities.sql_database import SQLDatabase

# Carregar variáveis de ambiente
load_dotenv()

def get_api_key():
    """Get API key from environment with proper error handling"""
    # Get API key from environment variable - never hardcode API keys
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        try:
            # Try to get from Streamlit secrets if environment variable is not set
            import streamlit as st
            api_key = st.secrets["OPENAI_API_KEY"]
        except (KeyError, ImportError, FileNotFoundError):
            pass
    
    if not api_key:
        raise ValueError(
            "❌ Erro: OPENAI_API_KEY não encontrada nas variáveis de ambiente ou nos secrets do Streamlit. "
            "Configure a chave da API em uma das seguintes formas:\n"
            "1. No arquivo .env como OPENAI_API_KEY=sua-chave\n"
            "2. Nas secrets do Streamlit (.streamlit/secrets.toml) como OPENAI_API_KEY=sua-chave"
        )
    return api_key

class OpenAISQLQuery:
    def __init__(self, db_path=None):
        """
        Inicializa o sistema de consulta SQL simples usando OpenAI.
        
        Args:
            db_path (str, optional): Caminho para o arquivo do banco de dados.
                                    Se não fornecido, tenta localizar na pasta de trabalho.
        """
        # Obter a chave da API usando a função auxiliar
        self.api_key = get_api_key()
        
        # Inicializar o cliente OpenAI com a chave da API do ambiente
        self.client = OpenAI(api_key=self.api_key)
        
        # Localizar o banco de dados
        if db_path is None:
            possible_paths = [
                os.path.join(os.getcwd(), 'cargas.db'),
                '/home/ubuntu/sql_agent/cargas.db',
                '/Users/tgt/Documents/GitHub/agente_sql/cargas.db'
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    db_path = path
                    break
            else:
                raise FileNotFoundError("❌ Erro: O arquivo do banco de dados não foi encontrado em nenhum dos caminhos predefinidos.")
        
        self.db_path = db_path
        self.memory = []  # Manter histórico de consultas
        
        # Inicializar a conexão com o banco de dados SQL
        db_uri = f"sqlite:///{db_path}"
        self.db = SQLDatabase.from_uri(db_uri)
        
        # Carregar metadados do banco de dados
        self.metadata = self._load_metadata()
        
        # Criar o contexto para as consultas SQL
        self.context = self._create_context()
    
    def _load_metadata(self):
        """
        Carrega os metadados das tabelas de mapeamento do banco de dados.
        
        Returns:
            dict: Dicionário contendo os metadados das tabelas.
        """
        metadata = {
            "sentido": {},
            "portos": {},
            "paises_origem": {},
            "paises_destino": {},
            "tipo_navegacao": {},
            "natureza_carga": {},
            "conteiner_estado": {},
            "mercadorias": {},
            "anos_disponiveis": []
        }
        
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Carregar mapeamentos de Sentido
            cursor.execute("SELECT codigo, descricao FROM Sentido")
            for codigo, descricao in cursor.fetchall():
                metadata["sentido"][codigo] = descricao
            
            # Carregar mapeamentos de Portos
            cursor.execute("SELECT codigo, nome FROM Portos")
            for codigo, nome in cursor.fetchall():
                metadata["portos"][codigo] = nome
            
            # Carregar mapeamentos de Países de Origem
            cursor.execute("SELECT codigo, nome FROM PaisesOrigem")
            for codigo, nome in cursor.fetchall():
                metadata["paises_origem"][codigo] = nome
            
            # Carregar mapeamentos de Países de Destino
            cursor.execute("SELECT codigo, nome FROM PaisesDestino")
            for codigo, nome in cursor.fetchall():
                metadata["paises_destino"][codigo] = nome
            
            # Carregar mapeamentos de Tipo de Navegação
            cursor.execute("SELECT codigo, descricao FROM TipoNavegacao")
            for codigo, descricao in cursor.fetchall():
                metadata["tipo_navegacao"][codigo] = descricao
            
            # Carregar mapeamentos de Natureza da Carga
            cursor.execute("SELECT codigo, descricao FROM NaturezaCarga")
            for codigo, descricao in cursor.fetchall():
                metadata["natureza_carga"][codigo] = descricao
            
            # Carregar mapeamentos de Estado do Contêiner
            cursor.execute("SELECT codigo, descricao FROM ConteinerEstado")
            for codigo, descricao in cursor.fetchall():
                metadata["conteiner_estado"][codigo] = descricao
            
            # Carregar mapeamentos de Mercadorias
            cursor.execute("SELECT codigo, descricao FROM CDMercadoria")
            for codigo, descricao in cursor.fetchall():
                metadata["mercadorias"][codigo] = descricao
            
            # Obter anos disponíveis
            cursor.execute("SELECT DISTINCT Ano FROM Cargas ORDER BY Ano")
            metadata["anos_disponiveis"] = [ano[0] for ano in cursor.fetchall()]
            
            conn.close()
        except Exception as e:
            print(f"Erro ao carregar metadados: {e}")
        
        return metadata
    
    def _create_context(self):
        """
        Cria o contexto para as consultas SQL com base nos metadados.
        
        Returns:
            str: Contexto para as consultas SQL.
        """
        # Obter o esquema do banco de dados
        db_schema = self.db.get_table_info()
        
        # Criar o contexto com o esquema e os metadados
        context = f"""
Você é um assistente especializado em traduzir consultas em linguagem natural para SQL para um banco de dados de cargas portuárias.

ESQUEMA DO BANCO DE DADOS:
{db_schema}

IMPORTANTE: Ao analisar consultas em linguagem natural, você deve entender o contexto e os termos específicos:

1. SENTIDO DAS CARGAS:
   - "Embarcados" ou "embarcadas" refere-se a exportações (código 2 na tabela Sentido, valor "Embarcados" na coluna Sentido da tabela Cargas)
   - "Desembarcados" ou "desembarcadas" refere-se a importações (código 1 na tabela Sentido, valor "Desembarcados" na coluna Sentido da tabela Cargas)
   - "Movimentadas" ou "movimentação" refere-se ao total de cargas, incluindo TANTO exportações (Embarcados) QUANTO importações (Desembarcados)

2. MÉTRICAS DE QUANTIDADE:
   - "Toneladas" refere-se à coluna "VLPesoCargaBruta" na tabela Cargas
   - "TEUs" refere-se à coluna "TEU" na tabela Cargas (Twenty-foot Equivalent Unit, medida para contêineres)
   - "Quantidade" ou "volume" geralmente se refere à coluna "VLPesoCargaBruta", mas pode se referir a "QTCarga" dependendo do contexto

3. PORTOS:
   - Quando mencionarem nomes de portos como "Porto do Itaqui", você deve relacionar com o código correspondente (ex: "BRIQI" para Itaqui)
   - Outros códigos importantes: "BRPNG" para Paranaguá, "BRANT" para Antonina, "BRSSZ" para Santos
   - Para o Porto de Santos, considere também o terminal "DP World Santos" com código "BRSP008"
   - Verifique se o porto está na origem ou no destino da carga

4. PAÍSES:
   - Quando mencionarem nomes de países, relacione com os códigos correspondentes nas tabelas PaisesOrigem e PaisesDestino
   - Verifique se o país está na origem (Pais_Origem) ou no destino (Pais_Destino) da carga

5. TIPOS DE NAVEGAÇÃO:
   - "Cabotagem" refere-se ao transporte entre portos do mesmo país (código 3 na tabela TipoNavegacao)
   - "Longo curso" refere-se ao transporte internacional (código 5 na tabela TipoNavegacao)
   - "Navegação interior" refere-se ao transporte em rios e lagos (código 1 na tabela TipoNavegacao)
   - "Apoio marítimo" refere-se a embarcações de apoio offshore (código 4 na tabela TipoNavegacao)
   - "Apoio portuário" refere-se a embarcações que operam dentro do porto (código 2 na tabela TipoNavegacao)

6. NATUREZA DA CARGA:
   - "Granel sólido" refere-se a cargas como minério, grãos, etc.
   - "Granel líquido" refere-se a cargas como petróleo, combustíveis, etc.
   - "Carga geral" refere-se a cargas diversas não classificadas como granel
   - "Carga conteinerizada" refere-se a cargas transportadas em contêineres

7. MERCADORIAS:
   - Quando mencionarem tipos específicos de mercadorias, relacione com os códigos na tabela CDMercadoria
   - Exemplos: "animais vivos", "petróleo", "veículos", etc.

8. PERÍODOS DE TEMPO:
   - "Mensal" ou "por mês" significa agrupar por mês usando a função strftime('%m', Ano)
   - "Trimestral" ou "por trimestre" significa agrupar por trimestre
   - "Semestral" ou "por semestre" significa agrupar por semestre
   - "Anual" ou "por ano" significa agrupar por ano

9. COMPARAÇÕES:
   - "Mais que", "maior que", "acima de" significa usar o operador >
   - "Menos que", "menor que", "abaixo de" significa usar o operador <
   - "Entre" significa usar BETWEEN ou combinação de > e <

10. AGREGAÇÕES:
    - "Total", "soma" significa usar a função SUM()
    - "Média" significa usar a função AVG()
    - "Máximo" significa usar a função MAX()
    - "Mínimo" significa usar a função MIN()
    - "Contagem" significa usar a função COUNT()

11. ANOS:
    - Os dados disponíveis são para os seguintes anos: {', '.join(self.metadata["anos_disponiveis"])}
    - Se perguntarem sobre anos não disponíveis, informe que não há dados para esse período
    - Ao processar consultas que especificam um ano, sempre considere o período completo do ano (de 01/01 a 31/12)

12. CONSIDERAÇÕES GERAIS:
    - IMPORTANTE: Para TODAS as consultas sobre portos, cargas, períodos ou qualquer outro critério específico, SEMPRE aplique a lógica de consulta ampliada demonstrada nos exemplos abaixo
    - Ao processar consultas sobre portos específicos, considere TODOS os terminais relacionados àquele porto (públicos e privados)
    - Para consultas sobre Santos, inclua tanto o código "BRSSZ" quanto "BRSP008" (DP World Santos)
    - Para consultas sobre qualquer porto, verifique se o porto está na origem (para exportações) ou no destino (para importações)
    - SEMPRE amplie as consultas para capturar mais dados relevantes, usando técnicas como LIKE para nomes parciais (ex: '%santos%', '%terminal%', '%porto%')
    - Para consultas sobre períodos, SEMPRE considere o período completo (ex: para um ano, use BETWEEN '2023-01-01' AND '2023-12-31')
    - Para consultas sobre tipos de carga, use LIKE com padrões amplos para capturar todas as variações relevantes
    - Quando relevante, agrupe os resultados por critérios significativos (ex: por sentido, por mês, por tipo de carga)
    - Sempre inclua contagens (COUNT) além de somas (SUM) para fornecer contexto adicional sobre os dados

EXEMPLOS DE CONSULTAS:

1. "Quantas toneladas foram embarcadas pelo Porto do Itaqui em 2023?"
   SQL: 
   ```sql
   SELECT SUM(VLPesoCargaBruta) as total_toneladas, COUNT(*) as total_registros
   FROM Cargas
   WHERE Sentido = 'Embarcados' AND Origem = 'BRIQI' AND Ano = '2023'
   ```

2. "Qual o total de carga desembarcada em Santos em 2023?"
   SQL:
   ```sql
   SELECT SUM(VLPesoCargaBruta) as total_toneladas, COUNT(*) as total_registros
   FROM Cargas
   WHERE Sentido = 'Desembarcados' AND Destino IN ('BRSSZ', 'BRSP008') AND Ano = '2023'
   ```

3. "Quantos TEUs de contêineres foram movimentados em 2023?"
   SQL:
   ```sql
   SELECT SUM(TEU) as total_teus, COUNT(*) as total_registros
   FROM Cargas
   WHERE Ano = '2023'
   ```

4. "Qual o volume de granéis líquidos exportados em 2023?"
   SQL:
   ```sql
   SELECT SUM(VLPesoCargaBruta) as total_toneladas, COUNT(*) as total_registros
   FROM Cargas
   WHERE Natureza_da_Carga = 'Granel Líquido e Gasoso' AND Sentido = 'Embarcados' AND Ano = '2023'
   ```

5. "Quais os 5 principais países de destino das exportações brasileiras em 2023?"
   SQL:
   ```sql
   SELECT Pais_Destino, SUM(VLPesoCargaBruta) as total_toneladas, COUNT(*) as total_registros
   FROM Cargas
   WHERE Sentido = 'Embarcados' AND Ano = '2023'
   GROUP BY Pais_Destino
   ORDER BY total_toneladas DESC
   LIMIT 5
   ```

Sua tarefa é:
1. Analisar a consulta em linguagem natural
2. Gerar uma consulta SQL válida que responda à pergunta
3. Fornecer uma explicação clara da consulta SQL gerada
4. Retornar APENAS a consulta SQL sem comentários adicionais

Responda APENAS com a consulta SQL, sem nenhum texto adicional.
"""
        return context
    
    def process_query(self, query):
        """
        Processa uma consulta em linguagem natural e retorna a consulta SQL correspondente.
        
        Args:
            query (str): Consulta em linguagem natural.
            
        Returns:
            dict: Dicionário contendo a consulta original, a consulta SQL gerada e o resultado.
        """
        try:
            # Criar a mensagem para o modelo
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": self.context},
                    {"role": "user", "content": query}
                ]
            )
            
            # Extrair a consulta SQL da resposta
            sql_query = response.choices[0].message.content.strip()
            
            # Remover marcadores de código SQL se presentes
            if sql_query.startswith("```sql"):
                sql_query = sql_query[6:]
            if sql_query.endswith("```"):
                sql_query = sql_query[:-3]
            
            sql_query = sql_query.strip()
            
            # Executar a consulta SQL
            result = self.db.run(sql_query)
            
            # Armazenar no histórico
            self.memory.append({
                "query": query,
                "sql": sql_query,
                "result": result
            })
            
            return {
                "query": query,
                "sql": sql_query,
                "result": result
            }
        except Exception as e:
            print(f"Erro ao processar consulta: {e}")
            error_message = f"Erro: {str(e)}"
            self.memory.append({
                "query": query,
                "sql": "Error generating SQL",
                "result": error_message
            })
            return {
                "query": query,
                "sql": "Error generating SQL",
                "result": error_message
            }
    
    def get_memory(self):
        """
        Retorna o histórico de consultas processadas.
        
        Returns:
            list: Lista de dicionários contendo as consultas processadas.
        """
        return self.memory

# Exemplo de uso
if __name__ == "__main__":
    try:
        # Inicializar o sistema de consulta SQL
        sql_query = OpenAISQLQuery()
        print("✅ Sistema de consulta SQL inicializado com sucesso!")
        
        # Testar uma consulta simples
        test_query = "Quantas cargas foram registradas no ano de 2023?"
        print(f"\nExecutando consulta de teste: '{test_query}'")
        
        response = sql_query.process_query(test_query)
        
        print("\n--- Resultado da Consulta ---")
        print(f"Consulta: {response['query']}")
        print(f"SQL: {response['sql']}")
        print(f"Resultado: {response['result']}")
        print("-----------------------------")
        
        # Testar outra consulta
        test_query_2 = "Quais as 5 mercadorias mais frequentes?"
        print(f"\nExecutando consulta de teste: '{test_query_2}'")
        
        response_2 = sql_query.process_query(test_query_2)
        
        print("\n--- Resultado da Consulta ---")
        print(f"Consulta: {response_2['query']}")
        print(f"SQL: {response_2['sql']}")
        print(f"Resultado: {response_2['result']}")
        print("-----------------------------")
        
    except Exception as e:
        print(f"❌ Erro ao testar o sistema de consulta SQL: {e}")
