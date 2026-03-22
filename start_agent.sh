#!/bin/bash
echo "Starting DeepLense Simulation Agent..."

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing requirements..."
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Ensure Ollama is reachable
if ! curl -s http://localhost:11434/v1/models > /dev/null; then
    echo "❌ ERROR: Ollama is not running on http://localhost:11434. Please start it before running the agent."
    exit 1
fi

echo "🚀 Launching Agent..."
python agent.py
