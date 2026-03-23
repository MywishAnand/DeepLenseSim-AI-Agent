# 🌌 DeepLense Simulation Agent

A conversational, context-aware agentic workflow for generating Gravitational Lensing images with the **DeepLenseSim** simulation pipeline. The agent 
- accepts and responds to user prompts in natural language with the Ollama 3.2B model.
- orchestrates the calls to DeepLenseSim via Pydantic AI.
- generates images in .npy (with structured metadata) and .png (for visualisation) formats.
- supports all four model configurations of DeepLenseSim.
- includes Human-in-the-loop component and follow-up questions for clarifications before execution.
- comprises a contextual guard to prevent any guessing or hallucinations by the Ollama model.

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
## How to use
1. Start Ollama with ```ollama pull llama3.2```.
2. Run ```bash source venv/bin/activate```.
3. Start the agent: ```bash python agent.py```.
4. Give prompt describing the desired simulation (e.g., substructure type, number of images, redshifts, etc.).
   Prompt example: "Generate 3 Model IV simulations with cdm, halo mass 2e12, and sigma_v 280."

## 📂 Project Structure
- `agent.py`: Main Pydantic AI agent logic & chat loop.
- `tools.py`: Simulation backend with Colossus stability patches.
- `Schemas.py`: Rigid Pydantic validation schemas.
- `DeepLenseSim/`: Submodule containing the core physics library.
- `Tests/README.md`: Master list of 20 verification prompts, this agent has been tested on.
- `Tests/`: Simulation outputs of the test prompts.
- `output/`: Functional directory for subsequent simulation outputs (ignored by git).

## 🛡️ Hardened Safety Features
- **Hardened Human-in-the-Loop**: The agent is now strictly forbidden from guessing core parameters. It will actively explain constraint violations (e.g., $z_{gal} \leq z_{halo}$) back to the user.
- **Redshift Limits**: Strictly enforces $z_{gal} \leq 1.0$ across all models with Pydantic-level validation.
- **Numerical Stability**: Injected `colossus` global cosmology (`planck15`) to prevent backend interpolation crashes.
- **Model IV Synthesis**: Support for multi-band Euclid images with advanced simulation parameters (`sigma_v`, etc.).
