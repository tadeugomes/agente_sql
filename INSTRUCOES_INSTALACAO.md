# Instruções para Execução Local do Agente SQL em Linguagem Natural

Este documento contém instruções detalhadas para instalar e executar o Agente SQL em Linguagem Natural em sua máquina local.

## Requisitos do Sistema

- Python 3.8 ou superior
- Pip (gerenciador de pacotes Python)
- Aproximadamente 100MB de espaço em disco para a aplicação e banco de dados

## Passo 1: Preparar o Ambiente

1. Crie uma pasta para o projeto:
   ```
   mkdir agente-sql
   cd agente-sql
   ```

2. (Opcional) Crie um ambiente virtual Python:
   ```
   python -m venv venv
   ```

3. Ative o ambiente virtual:
   - No Windows:
     ```
     venv\Scripts\activate
     ```
   - No macOS/Linux:
     ```
     source venv/bin/activate
     ```

## Passo 2: Instalar Dependências

Execute o seguinte comando para instalar todas as dependências necessárias:

```
pip install streamlit pandas
```

## Passo 3: Executar a Aplicação

1. Navegue até a pasta onde você extraiu os arquivos do projeto
2. Execute o comando:
   ```
   streamlit run app.py
   ```
3. A aplicação será iniciada e abrirá automaticamente em seu navegador padrão
4. Se o navegador não abrir automaticamente, acesse: http://localhost:8501

## Estrutura de Arquivos

Certifique-se de que todos os seguintes arquivos estejam presentes na pasta do projeto:

- `app.py`: Aplicação Streamlit principal
- `database_tools.py`: Ferramentas para interação com o banco de dados
- `sql_agent.py`: Agente para tradução de linguagem natural para SQL
- `utils.py`: Funções utilitárias para a interface
- `cargas.db`: Banco de dados SQLite com os dados de exemplo
- `static/css/style.css`: Estilos CSS personalizados

## Solução de Problemas

### Problema: A aplicação não inicia

**Solução 1**: Verifique se todas as dependências foram instaladas corretamente:
```
pip install -r requirements.txt
```

**Solução 2**: Verifique se o Python está no PATH do sistema:
```
python --version
```

**Solução 3**: Tente executar com uma porta diferente:
```
streamlit run app.py --server.port=8502
```

### Problema: Erro ao carregar o banco de dados

**Solução 1**: Verifique se o arquivo `cargas.db` está na mesma pasta que o arquivo `app.py`

**Solução 2**: Verifique as permissões do arquivo de banco de dados:
```
chmod 644 cargas.db
```

### Problema: Interface sem estilo/CSS

**Solução**: Certifique-se de que a pasta `static/css` existe e contém o arquivo `style.css`

### Problema: Erro "ModuleNotFoundError"

**Solução**: Instale o módulo faltante:
```
pip install [nome_do_modulo]
```

## Configurações Avançadas

Para personalizar a execução do Streamlit, você pode criar um arquivo `.streamlit/config.toml` com o seguinte conteúdo:

```toml
[theme]
primaryColor = "#1E3A8A"
backgroundColor = "#f5f7f9"
secondaryBackgroundColor = "#EFF6FF"
textColor = "#262730"
font = "sans serif"

[server]
enableCORS = true
enableXsrfProtection = false
maxUploadSize = 50
```

## Contato e Suporte

Se você encontrar problemas adicionais, verifique se todos os arquivos foram extraídos corretamente e se as dependências foram instaladas. 

Para mais informações sobre o Streamlit, consulte a [documentação oficial](https://docs.streamlit.io/).
