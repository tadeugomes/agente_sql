# Agente SQL em Linguagem Natural - Documentação

## Visão Geral

Este projeto implementa um agente de IA local capaz de processar consultas em linguagem natural e traduzi-las para comandos SQL. O sistema utiliza um banco de dados SQLite para armazenar e consultar dados de cargas, com uma interface Streamlit para interação com o usuário.

## Estrutura do Projeto

```
/home/ubuntu/sql_agent/
├── app.py                  # Interface Streamlit
├── create_database.py      # Script para criar e popular o banco de dados
├── database_tools.py       # Ferramentas para interação com o banco de dados
├── sql_agent.py            # Agente para tradução de linguagem natural para SQL
├── test_agent.py           # Testes para o agente SQL
├── test_database.py        # Testes para as ferramentas de banco de dados
└── cargas.db               # Banco de dados SQLite
```

## Componentes Principais

### 1. Banco de Dados SQLite

O banco de dados contém as seguintes tabelas:
- `Cargas`: Tabela principal com dados de cargas (50.000 registros de amostra)
- `CDMercadoria`: Códigos e descrições de mercadorias
- `Portos`: Códigos e nomes de portos
- `PaisesOrigem`: Códigos e nomes de países de origem
- `PaisesDestino`: Códigos e nomes de países de destino
- `TipoNavegacao`: Códigos e descrições de tipos de navegação
- `Sentido`: Códigos e descrições de sentidos (embarque/desembarque)
- `NaturezaCarga`: Códigos e descrições de naturezas de carga
- `ConteinerEstado`: Códigos e descrições de estados de contêiner

### 2. Ferramentas de Interação com o Banco de Dados

A classe `DatabaseTools` fornece métodos para:
- Listar tabelas disponíveis
- Descrever a estrutura de uma tabela
- Amostrar linhas de uma tabela
- Executar consultas SQL diretamente

### 3. Agente SQL

A classe `SQLAgent` implementa:
- Tradução de consultas em linguagem natural para SQL
- Execução de consultas SQL
- Armazenamento de histórico de consultas

### 4. Interface do Usuário

A interface Streamlit oferece:
- Campo para entrada de perguntas em linguagem natural
- Exibição da consulta SQL gerada
- Visualização dos resultados em tabelas
- Acesso ao esquema do banco de dados
- Histórico de interações

## Como Executar

1. Certifique-se de que todas as dependências estão instaladas:
   ```
   pip install langchain langchain-community pandas streamlit
   ```

2. Execute a aplicação Streamlit:
   ```
   streamlit run /home/ubuntu/sql_agent/app.py
   ```

## Limitações e Considerações

- A implementação atual do agente SQL utiliza uma abordagem baseada em regras para traduzir consultas em linguagem natural para SQL, em vez de um modelo de linguagem completo, devido a limitações de espaço em disco.
- O banco de dados contém uma amostra de 50.000 registros do conjunto de dados original para fins de teste.
- As consultas suportadas são limitadas aos padrões implementados no agente SQL.

## Exemplos de Consultas

O agente pode responder a perguntas como:
- "Quantas cargas foram registradas em 2023?"
- "Quais são as 5 mercadorias mais frequentes?"
- "Qual é o peso médio das cargas por tipo de navegação?"
- "Quais são as principais origens e destinos?"
- "Quais são as naturezas de carga mais comuns?"
