#!/bin/bash

# Deactivate the current virtual environment if it's active
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "Deactivating current virtual environment..."
    deactivate
fi

# Remove the old virtual environment
echo "Removing old virtual environment..."
rm -rf venv

# Create a new virtual environment
echo "Creating new virtual environment..."
python3 -m venv venv

# Activate the new virtual environment
echo "Activating new virtual environment..."
source venv/bin/activate

# Install packages with special handling for NumPy
echo "Installing packages..."
pip install streamlit==1.44.0
pip install --no-binary numpy numpy==1.26.3
pip install pandas==2.0.3
pip install langchain langchain-google-genai sqlalchemy python-dotenv

echo "Environment setup complete. Try running your application now."
