import asyncio
from pydantic_ai import Agent, RunContext
from schemas import SimulationConfig
from tools import run_deeplensesim

from dataclasses import dataclass

@dataclass
class AgentDeps:
    user_prompt: str

# Define the system prompt with clear instructions for the human-in-the-loop fallback.
SYSTEM_PROMPT = """
You are an expert astrophysicist AI assistant for the DeepLense project. 
Your primary goal is to help users generate strong lensing simulations using the `run_deeplens_simulation` tool.

### 🛡️ HUMAN-IN-THE-LOOP & SAFETY RULES
1. **NO GUESSING**: Do NOT assume values for `model_type`, `substructure`, `main_halo_mass`, `z_halo`, or `z_gal`.
2. **CLARIFICATION FIRST**: You MUST ask the user for missing details. If they just say "Run a simulation", you must NOT call the tool.
3. **MANDATORY DECLARATION**: The tool will check if the user actually typed these values. If you try to guess, the tool will REJECT your call.

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
    - If ANY are missing from the chat history, JUST ASK THE USER.
    """
    prompt = ctx.deps.user_prompt.lower()
    
    # Verification logic: Ensure the user actually mentioned the core parameters
    # This stops the LLM from 'guessing' defaults.
    mandatory_checks = {
        "model": ["model_i", "model_ii", "model_iii", "model_iv", "model 1", "model 2", "model 3", "model 4"],
        "substructure": ["cdm", "axion", "no_sub", "no substructure"],
        "mass": ["mass", "solar masses", "e11", "e12", "e13"]
    }
    
    missing = []
    if not any(keyword in prompt for keyword in mandatory_checks["model"]):
        missing.append("Model Type (I-IV)")
    if not any(keyword in prompt for keyword in mandatory_checks["substructure"]):
        missing.append("Substructure (CDM/Axion/No)")
    if not any(keyword in prompt for keyword in mandatory_checks["mass"]):
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
                
            # Pass the current input as deps so the tool can verify it
            deps = AgentDeps(user_prompt=user_input)
            
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

