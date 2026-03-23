# DeepLenseSim Agent: 20 Test Prompts

Following 20 prompts are run to verify the functionality, astronomy, and safety constraints of the **DeepLense Simulation Agent**. The output files in .png and .npy formats are shared here.

## 🔭 Basic Model & Instrument Verification
1. **Model I:** "Generate a Model I simulation with CDM substructure and a 1e12 halo mass."
2. **Model II:** "Run a Model II simulation with the Euclid instrument and no substructure."
3. **Model III:** "I need a Model III simulation (HST instrument) with CDM substructure and 1e12 mass."
4. **Model IV:** "Perform a Model IV multi-band synthesis using CDM substructure."

## 🌌 Substructure & Dark Matter Physics
5. **Axion Physics (Model II):** "Run a Model II Axion simulation. Use a vortex mass of 1e9 and an axion mass of 1e-22."
6. **Vortex Stress Test:** "Model III, Axion substructure, 1e-24 axion mass, 5e10 vortex mass."
7. **No Substructure:** "Model I, no_sub, 2e12 mass."
8. **Model IV CDM:** "Model IV with CDM substructure, 1e12 halo mass, and 1 simulation."

## 🛰️ Advanced Mathematical & Astro-Parameters
9. **Redshift Control & Stability:** "Model I, CDM, 1e12 mass, with z_halo set to 0.3 and z_gal set to 0.7." (Verified to work with the Colossus fix).
10. **Velocity Dispersion (Model IV):** "Run Model IV, CDM, 1e12 mass, and set sigma_v to 280."
11. **Source Offsets (Model IV):** "Model IV, no_sub, mass 1e12, source_pos_x 0.2 and source_pos_y -0.1."
12. **Rotation (Model IV):** "Model IV, CDM, 1e12 mass, source_angle 0.78 (radians)."

## 🛠️ Batch Processing & File Handling
13. **Multi-Image Run:** "Generate 5 simulations of Model I with no substructure and 1e12 mass."
14. **Batch Model IV:** "I need 3 multi-band images (Model IV) using CDM and 5e11 mass."
15. **High-Stress Batch:** "Generate 10 simulations for Model II Euclid."

## 🛡️ Human-in-the-Loop & Constraint Testing
16. **Missing Model:** "Run a simulation with 1e12 mass and CDM substructure."
17. **Missing Mass:** "Run a Model III simulation with no substructure."
18. **The "Everything" Vague Prompt:** "I want to run a gravitational lensing simulation for my research."
19. **Redshift Constraint Violation:** "Model I, CDM, 1e12 mass, z_gal 1.5." (Should trigger Pydantic validation error).
20. **Halo Redshift Conflict:** "Model II, CDM, 1e12 mass, z_halo 0.8, z_gal 0.5." (Should trigger lens library error).
