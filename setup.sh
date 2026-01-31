#!/bin/bash

# Setup script for AI Chatbot
# This script helps set up the environment for the chatbot

echo "🤖 AI Chatbot Setup"
echo "=================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    if [ -f env.example ]; then
        cp env.example .env
        echo "✓ .env file created"
        echo ""
        echo "⚠️  IMPORTANT: Please edit .env and add your API keys:"
        echo "   - ANTHROPIC_API_KEY (get from https://console.anthropic.com/)"
        echo "   - OPENAI_API_KEY (get from https://platform.openai.com/api-keys)"
    else
        echo "⚠️  env.example not found. Please create .env manually."
    fi
else
    echo "✓ .env file already exists"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the chatbot:"
echo "  python3 chatbot_ai.py"
echo ""
echo "Or in VSCode:"
echo "  Press F5 to debug"
echo "  Or use the Run button in the editor"
