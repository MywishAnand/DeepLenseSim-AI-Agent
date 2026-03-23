# 🌌 DeepLenseSim AI Agent

A **context-aware, conversational agentic system** for generating **Gravitational Lensing simulations** using the **DeepLenseSim** pipeline.
###### Website: https://mywishanand.github.io/DeepLenseSim-AI-Agent/
---

## 🚀 Core Capabilities

- 💬 **Natural Language Interface**  
  Interact with the system using plain English via **Ollama (Llama 3.2B)**.

- 🧠 **Agentic Workflow Orchestration**  
  Uses **Pydantic AI** to structure, validate, and execute simulation pipelines.

- 🖼️ **Simulation Output Formats**  
  - `.npy` → Structured data with metadata  
  - `.png` → Visualization-ready outputs  

- ⚙️ **Full DeepLenseSim Coverage**  
  Supports **all four model configurations**.

- 👨‍💻 **Human-in-the-Loop Control**  
  Ensures user confirmation through follow-up questions before execution.

- 🛡️ **Anti-Hallucination Guardrails**  
  Prevents the LLM from guessing or fabricating simulation parameters.

---

## ✨ Unique Functionalities

- 🧠 **Contextual Guard (No Hallucination Zone)**

  Unlike typical AI agents, this system:

  - 🚫 **Cannot infer or guess parameters**
  - ✅ Injects **raw user prompts directly into simulation validation**
  - 🔍 Verifies explicit user input (e.g., model type, mass)
  
  👉 Result: **100% user-driven, verifiable simulations**


- ⚛️ **Physics-Strict Constraints**

  Built-in **astrophysical validation layer** using Pydantic:
  
  - 🌌 **Redshift Ordering Enforcement**  
    Rejects invalid configurations where:  
    `z_source > z_lens`
  
  - 📏 **Redshift Upper Bound**  
    Enforces:  
    `z ≤ 1.0` (instrument consistency)


- 🛠️ **Numerical Stability Enhancements**
  
  - Integrated **global cosmology (`planck15`) via `colossus`**
  - Prevents common interpolation crashes:  
    `x_new < 0.001`
  
  👉 Ensures **robust simulations across custom redshift inputs**


- 🌈 Model IV Multi-Band Synthesis
  
  - Dedicated pipeline for **RGB image generation**
  - Supports **Euclid-like simulations** using:
    - `g`, `r`, `i` bands

---

## ⚡ Quick Start

#### 1️⃣ Prerequisites

- 🧠 **Ollama** (with Llama 3.2 model)

  ```bash
  ollama pull llama3.2
  ```

* 🐍 **Python 3.9+**

---

#### 2️⃣ Installation

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

#### 3️⃣ Run the Agent

```bash
python agent.py
```

---

## 🧪 How to Use

1️⃣ Start Ollama:

   ```bash
   ollama run llama3.2
   ```

2️⃣ Activate environment:

   ```bash
   source venv/bin/activate
   ```

3️⃣ Launch the agent:

   ```bash
   python agent.py
   ```

4️⃣ Provide a simulation prompt:

   **Example:**

   ```
   Generate 3 Model IV simulations with cdm, halo mass 2e12, and sigma_v 280.
   ```

---

## 📂 Project Structure

```
├── agent.py              # Core agent logic & conversational loop
├── tools.py              # Simulation backend + stability patches
├── Schemas.py            # Pydantic validation schemas
├── DeepLenseSim/         # Physics simulation submodule
├── Tests/
│   ├── README.md         # 20 validation prompts
│   └── outputs/          # Verified simulation outputs
├── output/               # Generated results
```

---
