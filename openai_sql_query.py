"""
Este script implementa uma abordagem mais simples para consultas SQL em linguagem natural,
usando a API do OpenAI diretamente em vez de OpenRouter.
"""

import os
import sqlite3
from dotenv import load_dotenv
from openai import OpenAI
from langchain_community.utilities.sql_database import SQLDatabase
import streamlit as st

# Carregar variáveis de ambiente
load_dotenv()

def get_api_key():
    """Get API key from Streamlit secrets"""
    return st.secrets["OPENAI_API_KEY"]

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
        
        # Inicializar o cliente OpenAI com a chave da API
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
   ```