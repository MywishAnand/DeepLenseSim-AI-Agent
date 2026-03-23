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
## How to proceed
1. Start Ollama with ```ollama pull llama3.2```.
2. Run ```source venv/bin/activate```.
3. Start the agent: ```python agent.py```.
5. Give prompt describing the desired simulation (e.g., model number, substructure type, number of images, redshifts).
   Prompt example: "Generate 3 Model IV simulations with cdm, halo mass 2e12, and sigma_v 280."

## 📂 Project Structure
- `agent.py`: Main Pydantic AI agent logic & chat loop.
- `tools.py`: Simulation backend with Colossus stability patches.
- `Schemas.py`: Rigid Pydantic validation schemas.
- `DeepLenseSim/`: Submodule containing the core physics library.
- `Tests/README.md`: Master list of 20 verification prompts, the agent was tested upon.
- `Tests/`: Simulation outputs of the test prompts.
- `output/`: Directory for subsequent simulation outputs.

## ✨ Unique Features
- **🧠 Contextual Guard (No Hallucination Zone)**: Unlike standard AI agents, this system is **physically prohibited** from guessing parameters. It injects your raw prompt directly into the simulation tool to verify you actually typed the Model and Mass, ensuring 100% human-in-the-loop fidelity.
- **⚛️ Physics-Strict Constraints**: Automated Pydantic-level validation for astrophysical consistency:
    - **Redshift Ordering**: Rejects $z_{source} \leq z_{lens}$ with a scientific explanation.
    - **Redshift Capping**: Hard-capped at $z \leq 1.0$ for instrument consistency.
- **🛠️ Numerical Stabilization Patches**: Injected a global `colossus` background cosmology (`planck15`) in `tools.py`, preventing the "Interpolation Range" crashes (`x_new < 0.001`) common in custom-redshift simulations.
- **🌈 Model IV Multi-Band Synthesis**: Integrated a dedicated pipeline for **3-channel RGB synthesis** (`g`, `r`, `i` bands) for Model IV Euclid simulations.
