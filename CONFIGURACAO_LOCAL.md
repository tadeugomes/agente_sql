# Configuração Local do Agente SQL em Linguagem Natural

Este documento detalha os requisitos de configuração local para executar o Agente SQL em Linguagem Natural em sua máquina.

## Estrutura de Diretórios

A aplicação requer a seguinte estrutura de diretórios:

```
agente-sql/
├── .streamlit/
│   └── config.toml
├── static/
│   └── css/
│       └── style.css
├── app.py
├── database_tools.py
├── sql_agent.py
├── utils.py
├── cargas.db
├── requirements.txt
└── setup_local.py
```

## Arquivos de Configuração

### .streamlit/config.toml

Este arquivo configura a aparência e comportamento do Streamlit:

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

### static/css/style.css

Este arquivo contém os estilos personalizados para a aplicação:

```css
/* Custom styles for the SQL Agent web application */
.sql-result {
    border-radius: 5px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    margin-top: 1rem;
}

.header-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 1rem;
}

.app-header {
    color: #1E3A8A;
    font-weight: bold;
}

.query-box {
    border: 1px solid #CBD5E1;
    border-radius: 5px;
    padding: 1rem;
    background-color: #F8FAFC;
}

.info-box {
    background-color: #EFF6FF;
    border-left: 4px solid #1E3A8A;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 0 5px 5px 0;
}

.footer {
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid #E2E8F0;
    text-align: center;
    font-size: 0.8rem;
    color: #64748B;
}
```

## Configuração Automática

Para facilitar a configuração, incluímos um script `setup_local.py` que cria automaticamente todos os diretórios e arquivos de configuração necessários. Execute-o antes de iniciar a aplicação:

```
python setup_local.py
```

## Requisitos do Sistema

- **Sistema Operacional**: Windows, macOS ou Linux
- **Python**: Versão 3.8 ou superior
- **Memória RAM**: Mínimo de 4GB recomendado
- **Espaço em Disco**: Aproximadamente 100MB para a aplicação e banco de dados
- **Navegador**: Chrome, Firefox, Edge ou Safari atualizado

## Variáveis de Ambiente (Opcional)

Você pode configurar as seguintes variáveis de ambiente para personalizar o comportamento da aplicação:

- `STREAMLIT_SERVER_PORT`: Porta em que o servidor Streamlit será executado (padrão: 8501)
- `STREAMLIT_SERVER_HEADLESS`: Define se o navegador deve abrir automaticamente (True/False)

Exemplo de configuração no Windows:
```
set STREAMLIT_SERVER_PORT=8502
```

Exemplo de configuração no macOS/Linux:
```
export STREAMLIT_SERVER_PORT=8502
```

## Permissões de Arquivo

Certifique-se de que o usuário que executa a aplicação tenha permissões de leitura e escrita para todos os arquivos e diretórios do projeto, especialmente para o arquivo de banco de dados `cargas.db`.
