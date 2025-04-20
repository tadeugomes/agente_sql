# Agente SQL em Linguagem Natural

Este aplicativo permite fazer consultas em linguagem natural a um banco de dados de cargas portuárias. O agente de IA traduz perguntas em linguagem natural para SQL e retorna os resultados.

## Configuração Local

1. Clone o repositório:
   ```bash
   git clone https://github.com/tadeugomes/agente_sql.git
   cd agente_sql
   ```

2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure as variáveis de ambiente:
   - Crie um arquivo `.env` na raiz do projeto com o seguinte conteúdo:
     ```
     OPENAI_API_KEY=sua-chave-da-api-aqui
     GOOGLE_API_KEY=sua-chave-do-google-aqui  # Se necessário
     ```

5. Execute o aplicativo:
   ```bash
   streamlit run app.py
   ```

## Implantação no Streamlit Cloud

### Preparação para Implantação

1. Certifique-se de que o repositório esteja no GitHub.

2. Adicione o arquivo `.streamlit/secrets.toml` ao `.gitignore` para não expor suas chaves de API.

3. Certifique-se de que o arquivo `requirements.txt` esteja atualizado com todas as dependências necessárias.

### Configuração no Streamlit Cloud

1. Acesse [Streamlit Cloud](https://streamlit.io/cloud) e faça login com sua conta GitHub.

2. Clique em "New app" e selecione o repositório, branch e arquivo principal (app.py).

3. Configure os segredos (secrets):
   - Na página do seu aplicativo no Streamlit Cloud, clique em "Advanced settings".
   - Na seção "Secrets", adicione suas chaves de API no formato TOML:
     ```toml
     OPENAI_API_KEY = "sua-chave-da-api-aqui"
     GOOGLE_API_KEY = "sua-chave-do-google-aqui"  # Se necessário
     ```

4. Clique em "Deploy" para implantar o aplicativo.

### Solução de Problemas

Se você encontrar o erro `OPENAI_API_KEY não encontrada nas variáveis de ambiente`, verifique se:

1. As chaves de API estão corretamente configuradas nos segredos do Streamlit Cloud.
2. O código está configurado para buscar as chaves tanto das variáveis de ambiente quanto dos segredos do Streamlit.

## Estrutura do Projeto

- `app.py`: Aplicativo Streamlit principal
- `sql_agent.py`: Implementação do agente SQL usando LangChain
- `.streamlit/`: Configurações do Streamlit
- `requirements.txt`: Dependências do projeto

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
