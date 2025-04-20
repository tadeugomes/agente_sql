# 🤖 Agente SQL em Linguagem Natural - Estatístico Aquaviário

Este aplicativo Streamlit permite que você faça consultas em linguagem natural ao banco de dados de cargas do Estatístico Aquaviário (ANTAQ) para o ano de 2023. O agente de IA, utilizando modelos da OpenAI através do LangChain, traduzirá sua pergunta para SQL, executará a consulta no banco de dados SQLite e retornará os resultados.

## Funcionalidades

*   Consulta em linguagem natural ao banco de dados `cargas.db`.
*   Tradução da consulta para SQL usando LLMs (OpenAI).
*   Execução da consulta SQL no banco de dados SQLite.
*   Exibição dos resultados e da consulta SQL gerada.
*   Histórico das consultas realizadas na sessão.
*   Configuração segura da chave da API OpenAI via Streamlit Secrets.

## Pré-requisitos

*   Python 3.9+
*   Git

## Instalação

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/tadeugomes/agente_sql.git
    cd agente_sql
    ```

2.  **Crie e ative um ambiente virtual:** (Recomendado)
    ```bash
    # Exemplo usando venv
    python -m venv .venv
    source .venv/bin/activate  # Linux/macOS
    # OU
    # .venv\\Scripts\\activate  # Windows
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Isso instalará Streamlit, LangChain, OpenAI >= 1.0.0 e outras bibliotecas necessárias.)*

## Configuração da Chave da API OpenAI

Este aplicativo requer uma chave da API OpenAI para funcionar. A configuração é feita usando o sistema de "Secrets" do Streamlit, que funciona tanto para desenvolvimento local quanto para deploy no Streamlit Cloud.

**NÃO COLOQUE SUA CHAVE DIRETAMENTE NO CÓDIGO OU EM ARQUIVOS NÃO IGNORADOS PELO GIT.**

1.  **Obtenha sua chave:** Crie ou copie sua chave da API no painel da [OpenAI](https://platform.openai.com/account/api-keys). A chave deve começar com `sk-...`.

2.  **Configuração Local:**
    *   Crie o diretório `.streamlit` na raiz do projeto, caso não exista:
        ```bash
        mkdir -p .streamlit
        ```
    *   Crie um arquivo chamado `secrets.toml` dentro do diretório `.streamlit`:
        ```
        touch .streamlit/secrets.toml
        ```
    *   Abra o arquivo `.streamlit/secrets.toml` e adicione sua chave no seguinte formato:
        ```toml
        # .streamlit/secrets.toml

        OPENAI_API_KEY = "sua_chave_sk-..."
        ```
        Substitua `"sua_chave_sk-..."` pela sua chave real da API OpenAI.
    *   O arquivo `.streamlit/secrets.toml` já está incluído no `.gitignore` para evitar que sua chave seja enviada acidentalmente para o GitHub.

3.  **Configuração no Streamlit Cloud:**
    *   Após fazer o deploy do seu aplicativo no Streamlit Cloud.
    *   Vá para as configurações (Settings ⚙️) do seu aplicativo.
    *   Navegue até a seção "Secrets".
    *   Adicione uma nova variável secreta com o nome `OPENAI_API_KEY` e cole sua chave da API OpenAI como valor. O formato deve ser:
        ```toml
        OPENAI_API_KEY = "sua_chave_sk-..."
        ```
    *   Salve as configurações. O Streamlit Cloud injetará essa chave de forma segura no ambiente do seu aplicativo.

## Executando Localmente

1.  Certifique-se de que seu ambiente virtual está ativado.
2.  Verifique se você configurou o arquivo `.streamlit/secrets.toml` conforme as instruções acima.
3.  Execute o aplicativo Streamlit:
    ```bash
    streamlit run app.py
    ```
4.  Abra seu navegador no endereço fornecido (geralmente `http://localhost:8501`).

## Deploy no Streamlit Cloud

1.  Certifique-se de que seu código está atualizado no GitHub (sem incluir o arquivo `.streamlit/secrets.toml`).
2.  Conecte seu repositório GitHub ao Streamlit Cloud.
3.  Crie um novo aplicativo ou configure um existente para usar este repositório e a branch correta (`clean_main`).
4.  **Configure a chave da API** na seção "Secrets" das configurações do aplicativo no Streamlit Cloud, como descrito na seção de Configuração acima.
5.  Faça o deploy ou reinicie o aplicativo.

## Estrutura do Projeto

*   `app.py`: Arquivo principal da aplicação Streamlit.
*   `sql_agent.py`: Classe que encapsula a lógica do agente LangChain SQL.
*   `openai_sql_query.py`: Implementação alternativa usando a API OpenAI diretamente (pode ser usada para testes ou abordagens diferentes).
*   `requirements.txt`: Lista de dependências Python.
*   `cargas.db`: Banco de dados SQLite com os dados de 2023.
*   `.streamlit/secrets.toml`: (Local) Armazena a chave da API OpenAI (ignorada pelo Git).
*   `.gitignore`: Especifica arquivos e diretórios a serem ignorados pelo Git.
*   `README.md`: Esta documentação.

## Dependências Principais

- streamlit
- langchain
- openai
- python-dotenv
- sqlalchemy

## Segurança de API Keys

Este projeto inclui várias ferramentas para garantir a segurança das chaves de API:

### Prevenção de Vazamentos

1. **Pre-commit Hook**: Impede que chaves de API sejam acidentalmente commitadas.
   - Instale com: `./install_pre_commit_hook.sh`

2. **Arquivo .env.example**: Fornece um modelo para configuração de variáveis de ambiente sem expor chaves reais.

3. **Documentação de Segurança**: Consulte os seguintes arquivos para mais informações:
   - `API_KEY_SECURITY.md`: Melhores práticas para gerenciamento de chaves de API
   - `REMOVING_API_KEYS_FROM_GIT_HISTORY.md`: Instruções para remover chaves de API do histórico do Git

### Remoção de Chaves do Histórico Git

Se você acidentalmente commitou uma chave de API, use o script fornecido para removê-la:
```bash
./remove_api_key_from_history.sh
```

### Melhores Práticas

- Nunca comite chaves de API reais no repositório
- Use variáveis de ambiente ou secrets do Streamlit
- Revogue e gere novas chaves se suspeitar que foram expostas
- Verifique regularmente o histórico de commits para garantir que nenhuma chave foi exposta
