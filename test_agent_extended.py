import asyncio
from agent import deeplense_agent

async def test_agent_flows_extended():
    print("--- Test 4: HST specification (Model III) ---")
    prompt_3 = "Generate 1 strong lensing image using Model_III with no_sub and halo mass 5e11."
    result_3 = await deeplense_agent.run(prompt_3)
    print("Agent Response 3:", result_3.output)
    
    print("\\n--- Test 5: Multi-band specification (Model IV) ---")
    prompt_4 = "Simulate Model_IV with CDM substructure and a main halo mass of 2e12."
    result_4 = await deeplense_agent.run(prompt_4)
    print("Agent Response 4:", result_4.output)

if __name__ == "__main__":
    asyncio.run(test_agent_flows_extended())
