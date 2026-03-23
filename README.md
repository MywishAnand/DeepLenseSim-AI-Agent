# 🌌 DeepLense Simulation Agent

A context-aware, conversational, AI-powered agent for Gravitational Lensing simulations with the **DeepLenseSim** pipeline.

## 🚀 Quick Start

### 1. Prerequisites
- **Ollama**: Install and run Ollama with `llama3.2` pulled:
  ```bash
  ollama run llama3.2
  ```
- **Python 3.9+**

### 2. Installation
```bash
# Set up virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Run the Agent
```bash
python agent.py
```

## 🛡️ Hardened Safety Features
- **Hardened Human-in-the-Loop**: The agent is now strictly forbidden from guessing core parameters. It will actively explain constraint violations (e.g., $z_{gal} \leq z_{halo}$) back to the user.
- **Redshift Limits**: Strictly enforces $z_{gal} \leq 1.0$ across all models with Pydantic-level validation.
- **Numerical Stability**: Injected `colossus` global cosmology (`planck15`) to prevent backend interpolation crashes.
- **Model IV Synthesis**: Support for multi-band Euclid images with advanced simulation parameters (`sigma_v`, etc.).

## 📂 Project Structure
- `agent.py`: Main Pydantic AI agent logic & chat loop.
- `tools.py`: Simulation backend with Colossus stability patches.
- `Schemas.py`: Rigid Pydantic validation schemas.
- `DeepLenseSim/`: Submodule containing the core physics library.
- `Tests/README.md`: Master list of 20 verification prompts, this agent has been tested on.
- `Tests/`: Simulation outputs of the test prompts.
- `output/`: Functional directory for subsequent simulation outputs (ignored by git).
