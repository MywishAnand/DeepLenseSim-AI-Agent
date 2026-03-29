import asyncio
from pydantic_ai import Agent, RunContext
from schemas import SimulationConfig
from tools import run_deeplensesim

from dataclasses import dataclass

@dataclass
class AgentDeps:
    full_history: str

# Define the system prompt with clear instructions for the human-in-the-loop fallback.
SYSTEM_PROMPT = """
You are an expert astrophysicist AI assistant for the DeepLense project. 
Your primary goal is to help users generate high-fidelity gravitational lensing simulations.

### 🛡️ DECISIVENESS & SAFETY RULES
1. **NO GUESSING**: Do NOT assume values for `model_type`, `substructure`, `main_halo_mass`, `z_halo`, or `z_gal`.
2. **CLARIFICATION**: If parameters are missing, ask for them immediately. 
3. **EXECUTE WHEN READY**: Once you have gathered all 5 mandatory parameters (Model, Substructure, Mass, Z_halo, Z_gal), PROCEED TO EXECUTE the simulation immediately. Do not ask for further confirmation once the data is complete.
4. **CONTEXT AWARENESS**: The tool verifies the entire conversation history. If the user previously provided a value, it is considered valid for the current run.

### 📝 OUTPUT RULES
- Explicitly list ALL generated file paths (`.npy` and `.png`). Never summarize them.
"""

import os
os.environ['OPENAI_API_KEY'] = 'ollama'  # dummy key
os.environ['OPENAI_BASE_URL'] = 'http://localhost:11434/v1'

from pydantic_ai.models.openai import OpenAIModel

# Configure Ollama model using its OpenAI-compatible endpoint
ollama_model = OpenAIModel('llama3.2')

deeplense_agent = Agent(
    ollama_model,
    system_prompt=SYSTEM_PROMPT,
    deps_type=AgentDeps,
    retries=2
)

@deeplense_agent.tool
def run_deeplens_simulation(ctx: RunContext[AgentDeps], config: SimulationConfig) -> dict:
    """
    Run a set of strong gravitational lensing simulations using DeepLenseSim.
    
    ### CRITICAL CONSTRAINTS:
    - ONLY call this if the user EXPLICITLY provided: model_type, substructure, main_halo_mass, z_halo, and z_gal.
    - If ANY are missing from the conversation history, JUST ASK THE USER.
    """
    history = ctx.deps.full_history.lower()
    
    # Verification logic: Ensure the user actually mentioned the core parameters
    # This stops the LLM from 'guessing' defaults.
    mandatory_checks = {
        "model": ["model_i", "model_ii", "model_iii", "model_iv", "model 1", "model 2", "model 3", "model 4"],
        "substructure": ["cdm", "axion", "no_sub", "no substructure"],
        "mass": ["mass", "solar masses", "e11", "e12", "e13"]
    }
    
    missing = []
    if not any(keyword in history for keyword in mandatory_checks["model"]):
        missing.append("Model Type (I-IV)")
    if not any(keyword in history for keyword in mandatory_checks["substructure"]):
        missing.append("Substructure (CDM/Axion/No)")
    if not any(keyword in history for keyword in mandatory_checks["mass"]):
        missing.append("Main Halo Mass")
        
    if missing:
        return {
            "status": "error",
            "message": f"Tool call rejected. You missed mandatory parameters in the user's prompt: {', '.join(missing)}.",
            "details": "The Agent attempted to guess parameters that you did not provide. Please explicitly state them."
        }

    print(f"\\n[Tool Execution] Running {config.num_simulations} simulation(s) for {config.model_type} with {config.substructure} substructure...\\n")
    return run_deeplensesim(config)

async def chat_loop():
    print("Welcome to the DeepLenseSim Agent (Context-Aware Edition)!")
    print("Type 'exit' to quit.\\n")
    
    message_history = []
    
    while True:
        try:
            user_input = input("User >> ")
            if user_input.lower() in ("exit", "quit"):
                break
                
            # Pass the cumulative history as deps so the tool can verify it
            full_user_history = "\\n".join([m['content'] for m in message_history if hasattr(m, 'role') and m.role == 'user']) + "\\n" + user_input
            deps = AgentDeps(full_history=full_user_history)
            
            result = await deeplense_agent.run(
                user_input, 
                message_history=message_history,
                deps=deps
            )
            
            print(f"\\nAgent >> {result.output}\\n")
            message_history = result.all_messages()

            
        except KeyboardInterrupt:
            break
        except Exception as e:
            # Catching Pydantic validation errors or tool execution crashes
            error_msg = str(e)
            if "validation error" in error_msg.lower():
                print(f"\\nAgent >> [Constraint Error] The simulation parameters provided were invalid: {error_msg}. Please provide physically consistent values (e.g., z_gal > z_halo and z_gal <= 1.0).\\n")
            else:
                print(f"\\nAgent >> I encountered an issue processing your request: {error_msg}. Let's try again with different parameters.\\n")

if __name__ == "__main__":
    asyncio.run(chat_loop())

