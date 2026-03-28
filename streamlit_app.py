import streamlit as st
import asyncio
import os
import re
from agent import deeplense_agent, AgentDeps
from pydantic_ai.messages import ModelRequest, ModelResponse

# Page Config
st.set_page_config(
    page_title="DeepLense AI Agent",
    page_icon="🌌",
    layout="wide"
)

# Sidebar for Info & Hardening Status
with st.sidebar:
    st.title("🌌 DeepLense AI")
    st.markdown("---")
    st.status("🛡️ Hardened (No Hallucination)", state="complete")
    st.info("""
    **Mandatory Parameters:**
    - Model Type (I-IV)
    - Substructure (CDM/Axion/No)
    - Main Halo Mass
    - Redshifts (Z_halo, Z_gal)
    """)
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.session_state.pydantic_history = []
        st.rerun()

st.title("🔭 DeepLense Simulation Console")
st.caption("Agentic Workflow for Automated Gravitational Lensing Research")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []
if "pydantic_history" not in st.session_state:
    st.session_state.pydantic_history = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "images" in message:
            for img_path in message["images"]:
                if os.path.exists(img_path):
                    st.image(img_path, caption=os.path.basename(img_path))

# Helper to extract image paths from agent output
def extract_image_paths(text):
    # Regex to find .png paths mentioned in the text
    paths = re.findall(r'(/[^\s]+\.png)', text)
    # Also handle relative paths if mentioned
    rel_paths = re.findall(r'((\w+/)*\w+\.png)', text)
    combined = list(set(paths + [p[0] for p in rel_paths]))
    # Filter to only existing files
    return [p for p in combined if os.path.exists(p)]

# Chat Input
if prompt := st.chat_input("Ask for a simulation (e.g. 'Model I, CDM, 1e12 mass, z_halo 0.5, z_gal 1.0')"):
    # Display user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Agent Response
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("🌌 *Simulating...*")
        
        try:
            # Prepare Deps
            deps = AgentDeps(user_prompt=prompt)
            
            # Run Agent
            result = asyncio.run(deeplense_agent.run(
                prompt,
                message_history=st.session_state.pydantic_history,
                deps=deps
            ))
            output_text = result.output
            
            # Extract images
            images = extract_image_paths(output_text)
            
            # Update display
            message_placeholder.markdown(output_text)
            for img in images:
                st.image(img, caption=os.path.basename(img))
                
            # Update session state
            st.session_state.messages.append({
                "role": "assistant", 
                "content": output_text,
                "images": images
            })
            st.session_state.pydantic_history = result.all_messages()
            
        except Exception as e:
            error_msg = str(e)
            if "validation error" in error_msg.lower():
                final_error = f"⚠️ **Constraint Error**: The parameters provided were invalid. {error_msg}. Please ensure Z_gal > Z_halo."
            else:
                final_error = f"❌ **Error**: {error_msg}"
            
            message_placeholder.markdown(final_error)
            st.session_state.messages.append({"role": "assistant", "content": final_error})

st.markdown("---")
st.caption("Powered by Pydantic AI & DeepLenseSim. Developed for MywishAnand.")
