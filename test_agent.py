import asyncio
from agent import deeplense_agent

async def test_agent_flows():
    print("--- Test 1: Full CDM specification (Model I) ---")
    prompt_1 = "Generate 1 strong lensing image using Model_I with cdm substructure and a main halo mass of 1e12."
    result_1 = await deeplense_agent.run(prompt_1)
    print("Agent Response 1:", result_1.output)
    
    print("\\n--- Test 2: Full Axion specification (Model II) ---")
    prompt_2 = "Simulate an axion scenario using Model_II. Main halo mass 1e12, axion mass 1e-24, vortex mass 1e10."
    result_2 = await deeplense_agent.run(prompt_2)
    print("Agent Response 2:", result_2.output)
    
    print("\\n--- Test 3: Human in the loop (Missing Parameters) ---")
    prompt_3 = "I want to simulate a lens."
    result_3 = await deeplense_agent.run(prompt_3)
    print("Agent Response 3:", result_3.output)

if __name__ == "__main__":
    asyncio.run(test_agent_flows())
