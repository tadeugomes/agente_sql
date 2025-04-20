#!/bin/bash

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ Created .env file"
else
    echo "✅ .env file already exists"
fi

# Prompt for API key if not set
if ! grep -q "^OPENAI_API_KEY=sk-" .env; then
    echo ""
    echo "OpenAI API Key não encontrada no arquivo .env"
    echo "Por favor, insira sua OpenAI API Key (começa com 'sk-'):"
    read -r api_key
    
    if [[ $api_key == sk-* ]]; then
        # Replace the example API key with the provided one
        sed -i '' "s|^OPENAI_API_KEY=.*|OPENAI_API_KEY=$api_key|" .env
        echo "✅ API Key configurada com sucesso!"
    else
        echo "❌ API Key inválida! Deve começar com 'sk-'"
        exit 1
    fi
fi

# Make sure the script is executable
chmod +x remove_api_key_from_history.sh

echo ""
echo "✅ Configuração concluída!"
echo "Você pode rodar a aplicação agora."