# 🌌 DeepLense Simulation Agent (Context-Aware)

A hardened, astrophysicist-AI-powered agent for the **DeepLenseSim** pipeline.

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
- **Contextual Guard**: The agent is forbidden from guessing Model types or Halo masses. It will check your original message for mandatory parameters.
- **Redshift Validation**: Rejects any request where $z_{source} \leq z_{lens}$ or $z_{source} > 1.0$.
- **Model Support**: Full support for Model I (Standard), Model II (Euclid), Model III (HST), and Model IV (Multi-band synthetic).

## 📂 Project Structure
- `agent.py`: Main Pydantic AI agent logic & chat loop.
- `tools.py`: Simulation backend with Colossus stability patches.
- `schemas.py`: Rigid Pydantic validation schemas.
- `DeepLenseSim/`: Submodule containing the core physics library.
- `output/`: Generated `.npy` and `.png` files.

---

*This agent was developed to automate high-fidelity strong lensing research with human-in-the-loop oversight.*
