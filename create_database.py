import pandas as pd
import sqlite3
import json
import os

# Este script cria o banco de dados cargas.db com uma restrição de 10.000 registros
# para fins de desenvolvimento e teste. A restrição é implementada durante a importação
# dos dados do CSV.

# Definir caminhos dos arquivos
csv_path = os.path.join(os.getcwd(),'carga_encoded.csv')
json_path = os.path.join(os.getcwd(),'mapeamentos.json')
db_path = os.path.join(os.getcwd(),'cargas.db')

# Criar conexão com o banco de dados SQLite
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("Criando banco de dados SQLite...")

# Carregar os mapeamentos do arquivo JSON
with open(json_path, 'r') as f:
    mapeamentos = json.load(f)

# Criar tabelas para os mapeamentos
print("Criando tabelas de mapeamento...")

# Tabela para CDMercadoria
cursor.execute('''
CREATE TABLE IF NOT EXISTS CDMercadoria (
    codigo TEXT PRIMARY KEY,
    descricao TEXT
)
''')

# Tabela para Portos
cursor.execute('''
CREATE TABLE IF NOT EXISTS Portos (
    codigo TEXT PRIMARY KEY,
    nome TEXT
)
''')

# Tabela para Países Origem
cursor.execute('''
CREATE TABLE IF NOT EXISTS PaisesOrigem (
    codigo TEXT PRIMARY KEY,
    nome TEXT
)
''')

# Tabela para Países Destino
cursor.execute('''
CREATE TABLE IF NOT EXISTS PaisesDestino (
    codigo TEXT PRIMARY KEY,
    nome TEXT
)
''')

# Tabela para Tipo Navegação
cursor.execute('''
CREATE TABLE IF NOT EXISTS TipoNavegacao (
    codigo TEXT PRIMARY KEY,
    descricao TEXT
)
''')

# Tabela para Sentido
cursor.execute('''
CREATE TABLE IF NOT EXISTS Sentido (
    codigo TEXT PRIMARY KEY,
    descricao TEXT
)
''')

# Tabela para Natureza da Carga
cursor.execute('''
CREATE TABLE IF NOT EXISTS NaturezaCarga (
    codigo TEXT PRIMARY KEY,
    descricao TEXT
)
''')

# Tabela para ConteinerEstado
cursor.execute('''
CREATE TABLE IF NOT EXISTS ConteinerEstado (
    codigo TEXT PRIMARY KEY,
    descricao TEXT
)
''')

# Inserir dados nas tabelas de mapeamento
print("Inserindo dados nas tabelas de mapeamento...")

# Inserir dados na tabela CDMercadoria
for codigo, descricao in mapeamentos['CDMercadoria'].items():
    cursor.execute('INSERT OR REPLACE INTO CDMercadoria VALUES (?, ?)', (codigo, descricao))

# Inserir dados na tabela Portos
for codigo, nome in mapeamentos['Portos'].items():
    cursor.execute('INSERT OR REPLACE INTO Portos VALUES (?, ?)', (codigo, nome))

# Inserir dados na tabela PaisesOrigem
for codigo, nome in mapeamentos['Países Origem'].items():
    cursor.execute('INSERT OR REPLACE INTO PaisesOrigem VALUES (?, ?)', (codigo, nome))

# Inserir dados na tabela PaisesDestino
for codigo, nome in mapeamentos['Países Destino'].items():
    cursor.execute('INSERT OR REPLACE INTO PaisesDestino VALUES (?, ?)', (codigo, nome))

# Inserir dados na tabela TipoNavegacao
for codigo, descricao in mapeamentos['Tipo Navegação'].items():
    cursor.execute('INSERT OR REPLACE INTO TipoNavegacao VALUES (?, ?)', (codigo, descricao))

# Inserir dados na tabela Sentido
for codigo, descricao in mapeamentos['Sentido'].items():
    cursor.execute('INSERT OR REPLACE INTO Sentido VALUES (?, ?)', (codigo, descricao))

# Inserir dados na tabela NaturezaCarga
for codigo, descricao in mapeamentos['Natureza da Carga'].items():
    cursor.execute('INSERT OR REPLACE INTO NaturezaCarga VALUES (?, ?)', (codigo, descricao))

# Inserir dados na tabela ConteinerEstado
for codigo, descricao in mapeamentos['ConteinerEstado'].items():
    cursor.execute('INSERT OR REPLACE INTO ConteinerEstado VALUES (?, ?)', (codigo, descricao))

conn.commit()
print("Tabelas de mapeamento criadas e populadas com sucesso!")

# Criar tabela principal para os dados do CSV
print("Criando tabela principal para os dados do CSV...")

# Ler as primeiras linhas do CSV para obter os nomes das colunas
df_sample = pd.read_csv(csv_path, nrows=5)
colunas = df_sample.columns.tolist()

# Renomear colunas com nomes problemáticos para evitar ambiguidades e erros de sintaxe
column_mapping = {
    'Tipo Operação da Carga': 'TipoOperacaoCarga',
    'Tipo Navegação': 'TipoNavegacao_Codigo',
    'Tipo_Navegacao_Desc': 'TipoNavegacao_Desc',
    'Percurso Transporte em vias Interiores': 'PercursoTransporteViasInteriores',
    'Percurso Transporte Interiores': 'PercursoTransporteInteriores',
    'Carga Geral Acondicionamento': 'CargaGeralAcondicionamento'
}

# Criar a tabela principal usando nomes de colunas seguros
print("Criando tabela Cargas com nomes de colunas seguros...")

# Primeiro, criar uma lista de nomes de colunas SQL seguros
colunas_sql = []
for coluna in colunas:
    coluna_sql = column_mapping.get(coluna, coluna)
    # Substituir espaços e caracteres especiais
    coluna_sql = coluna_sql.replace(' ', '_').replace('-', '_')
    colunas_sql.append(coluna_sql)

# Criar a tabela principal
create_table_sql = '''
CREATE TABLE IF NOT EXISTS Cargas (
'''

# Adicionar colunas à tabela com nomes ajustados
for i, coluna in enumerate(colunas):
    coluna_sql = colunas_sql[i]
    
    if coluna in ['IDCarga', 'IDAtracacao']:
        create_table_sql += f'    "{coluna_sql}" INTEGER,'
    elif coluna in ['VLPesoCargaBruta', 'QTCarga', 'TEU']:
        create_table_sql += f'    "{coluna_sql}" REAL,'
    else:
        create_table_sql += f'    "{coluna_sql}" TEXT,'

# Adicionar chave primária e finalizar a criação da tabela
create_table_sql = create_table_sql.rstrip(',') + ',\n    PRIMARY KEY ("IDCarga")\n)'
cursor.execute(create_table_sql)

# Definir o limite de registros
max_rows = 10000  # Limite de 10.000 registros

print("Tabela principal criada com sucesso!")
print(f"Iniciando importação dos dados do CSV (limitado a {max_rows} registros)...")

# Atualizar o mapeamento de colunas para incluir todas as colunas
column_mapping_complete = {}
for i, coluna in enumerate(colunas):
    column_mapping_complete[coluna] = colunas_sql[i]

# Importar dados do CSV em chunks para economizar memória
chunksize = 5000
total_rows = 0

try:
    for chunk in pd.read_csv(csv_path, chunksize=chunksize):
        # Verificar se já atingimos o limite de registros
        if total_rows >= max_rows:
            break
            
        # Se este chunk fizer ultrapassar o limite, cortar o chunk
        if total_rows + len(chunk) > max_rows:
            chunk = chunk.iloc[:(max_rows - total_rows)]
            
        # Renomear colunas no DataFrame
        chunk = chunk.rename(columns=column_mapping_complete)
        
        # Preparar os dados para inserção
        records = chunk.to_dict('records')
        
        # Criar a query de inserção com nomes de colunas entre aspas
        placeholders = ', '.join(['?'] * len(colunas_sql))
        columns = ', '.join([f'"{col}"' for col in colunas_sql])
        insert_query = f'INSERT OR REPLACE INTO Cargas ({columns}) VALUES ({placeholders})'
        
        # Preparar os valores para inserção
        values = []
        for record in records:
            row_values = []
            for col in colunas_sql:
                row_values.append(record.get(col))
            values.append(tuple(row_values))
        
        # Inserir os dados
        cursor.executemany(insert_query, values)
        conn.commit()
        
        total_rows += len(records)
        print(f"Importados {total_rows} registros...")
        
        # Verificar novamente se atingimos o limite após a importação
        if total_rows >= max_rows:
            print(f"Limite de {max_rows} registros atingido. Importação concluída.")
            break
            
except Exception as e:
    print(f"Erro durante a importação: {e}")
    conn.rollback()
    raise

# Criar índices para melhorar o desempenho das consultas
print("Criando índices para otimizar consultas...")
cursor.execute('CREATE INDEX IF NOT EXISTS idx_cdmercadoria ON Cargas ("CDMercadoria")')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_origem ON Cargas ("Origem")')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_destino ON Cargas ("Destino")')
cursor.execute('CREATE INDEX IF NOT EXISTS idx_ano ON Cargas ("Ano")')

# Fechar a conexão
conn.commit()
conn.close()

print("Banco de dados criado e populado com sucesso!")
print(f"Caminho do banco de dados: {db_path}")
