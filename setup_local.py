import os

# Verifica se a pasta static/css existe e cria se não existir
os.makedirs('static/css', exist_ok=True)

# Verifica se o arquivo .streamlit/config.toml existe e cria se não existir
os.makedirs('.streamlit', exist_ok=True)

# Escreve o arquivo de configuração do Streamlit
with open('.streamlit/config.toml', 'w') as f:
    f.write("""
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
""")

# Escreve o arquivo CSS
with open('static/css/style.css', 'w') as f:
    f.write("""
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
""")

print("Arquivos de configuração criados com sucesso!")
