# Mapeamentos Semânticos do Agente SQL

Este documento descreve os mapeamentos semânticos implementados no agente SQL para permitir consultas em linguagem natural mais avançadas e contextuais.

## Mapeamentos Implementados

### 1. Sentido das Cargas
- **"Embarcados"** ou **"embarcadas"** → exportações (coluna `Sentido` = "Embarcados")
- **"Desembarcados"** ou **"desembarcadas"** → importações (coluna `Sentido` = "Desembarcados")

### 2. Métricas de Quantidade
- **"Toneladas"** → coluna `VLPesoCargaBruta`
- **"TEUs"** → coluna `TEU` (Twenty-foot Equivalent Unit, medida para contêineres)
- **"Quantidade"** ou **"volume"** → geralmente se refere à coluna `VLPesoCargaBruta`, mas pode se referir a `QTCarga` dependendo do contexto

### 3. Portos
- Nomes de portos como **"Porto do Itaqui"** → código correspondente (ex: "BRIQI")
- Verifica tanto a coluna `Origem` quanto `Destino` para encontrar o porto mencionado

### 4. Países
- Nomes de países → códigos correspondentes nas tabelas `PaisesOrigem` e `PaisesDestino`
- Verifica se o país está na origem (`Pais_Origem`) ou no destino (`Pais_Destino`) da carga

### 5. Tipos de Navegação
- **"Cabotagem"** → transporte entre portos do mesmo país (código 3 na tabela `TipoNavegacao`)
- **"Longo curso"** → transporte internacional (código 5 na tabela `TipoNavegacao`)
- **"Navegação interior"** → transporte em rios e lagos (código 1 na tabela `TipoNavegacao`)
- **"Apoio marítimo"** → embarcações de apoio offshore (código 4 na tabela `TipoNavegacao`)
- **"Apoio portuário"** → embarcações que operam dentro do porto (código 2 na tabela `TipoNavegacao`)

### 6. Natureza da Carga
- **"Granel sólido"** → cargas como minério, grãos, etc.
- **"Granel líquido"** → cargas como petróleo, combustíveis, etc.
- **"Carga geral"** → cargas diversas não classificadas como granel
- **"Carga conteinerizada"** → cargas transportadas em contêineres

### 7. Mercadorias
- Tipos específicos de mercadorias → códigos na tabela `CDMercadoria`
- Exemplos: "animais vivos", "petróleo", "veículos", etc.

### 8. Períodos de Tempo
- **"Mensal"** ou **"por mês"** → agrupar por mês usando a função `strftime('%m', Ano)`
- **"Trimestral"** ou **"por trimestre"** → agrupar por trimestre
- **"Semestral"** ou **"por semestre"** → agrupar por semestre
- **"Anual"** ou **"por ano"** → agrupar por ano

### 9. Comparações
- **"Mais que"**, **"maior que"**, **"acima de"** → operador `>`
- **"Menos que"**, **"menor que"**, **"abaixo de"** → operador `<`
- **"Entre"** → `BETWEEN` ou combinação de `>` e `<`

### 10. Agregações
- **"Total"**, **"soma"** → função `SUM()`
- **"Média"** → função `AVG()`
- **"Máximo"** → função `MAX()`
- **"Mínimo"** → função `MIN()`
- **"Contagem"** → função `COUNT()`

## Exemplos de Consultas Suportadas

1. **Consulta por tipo de mercadoria**:
   - "Quantas toneladas de animais vivos foram embarcadas em 2023?"

2. **Consulta por país**:
   - "Qual o volume de carga exportada do Brasil para a China em 2023?"

3. **Consulta por tipo de navegação**:
   - "Quantas cargas de cabotagem passaram pelo Porto de Santos em 2023?"

4. **Consulta por natureza da carga**:
   - "Qual o volume de granéis líquidos movimentados em 2023?"

5. **Consulta por TEUs**:
   - "Quantos TEUs foram movimentados pelo Porto de Santos em 2023?"

6. **Consulta com comparação**:
   - "Quais portos movimentaram mais de 500 mil toneladas em 2023?"

7. **Consulta com agregação**:
   - "Qual a média mensal de cargas embarcadas em 2023?"

8. **Consulta combinada**:
   - "Qual foi o porto que mais exportou granéis sólidos em 2023?"
   - "Quais os 5 principais países de destino das exportações brasileiras em 2023?"
   - "Qual a média trimestral de cargas de cabotagem em 2023?"

## Como Funciona

O agente SQL utiliza um contexto personalizado que inclui instruções específicas sobre como interpretar termos como "embarcados", "toneladas", nomes de portos, etc. Ele também carrega os metadados do banco de dados para fornecer informações precisas sobre os anos disponíveis e outros dados relevantes.

Quando uma consulta é feita, o agente analisa o contexto e gera a consulta SQL apropriada, levando em consideração os mapeamentos semânticos descritos acima.

## Extensibilidade

O sistema foi projetado para ser facilmente extensível. Novos mapeamentos semânticos podem ser adicionados modificando os métodos `_load_metadata()` e `_create_context()` na classe `SQLAgent`.
