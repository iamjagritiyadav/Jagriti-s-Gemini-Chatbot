import streamlit as st
import google.generativeai as genai

# --- 1. SETUP & SECRETS ---
# Access the key saved as GEMINI_API_KEY in your Streamlit dashboard
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except KeyError:
    st.error("Missing Secret: Please add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    st.stop()

# Page configuration
st.set_page_config(page_title="Jagriti's Chatbot", layout="centered", page_icon="J")
st.title("Jagriti's Chatbot")

# --- 2. DYNAMIC MODEL FINDER ---
@st.cache_resource
def get_best_model():
    try:
        available_models = [
            m.name for m in genai.list_models() 
            if 'generateContent' in m.supported_generation_methods
        ]
        
        # Prioritize Flash models for speed
        for name in available_models:
            if "flash" in name.lower():
                return name
        
        return available_models[0] if available_models else "models/gemini-1.5-flash"
    except Exception as e:
        st.error(f"Failed to fetch models: {e}")
        return "models/gemini-1.5-flash"

working_model_name = get_best_model()
st.caption(f"Powered by: `{working_model_name}`")

# --- 3. CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. CHAT LOGIC ---
if prompt := st.chat_input("How can I help you today?"):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Assistant Response
    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel(working_model_name)
            response = model.generate_content(prompt, stream=True)
            
            full_res = ""
            placeholder = st.empty()
            
            for chunk in response:
                if chunk.text:
                    full_res += chunk.text
                    # Cursor effect for a better UI feel
                    placeholder.markdown(full_res + "▌")
            
            placeholder.markdown(full_res)
            # Save assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            
        except Exception as e:
            st.error(f"An error occurred: {e}")
