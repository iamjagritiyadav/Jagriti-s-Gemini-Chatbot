import streamlit as st
import google.generativeai as genai

# --- 1. SETUP ---
# Paste your API Key here
API_KEY = "....."
genai.configure(api_key=API_KEY)

st.set_page_config(page_title="Gemini Chatbot", layout="centered")
st.title("Jagriti's Gemini Chatbot")

# --- 2. DYNAMIC MODEL FINDER (The 404 Fix) ---
@st.cache_resource
def get_best_model():
    try:
        # This lists every model your API key is allowed to use
        available_models = [
            m.name for m in genai.list_models() 
            if 'generateContent' in m.supported_generation_methods
        ]
        
        # We try to find 'flash' first because it's fast/free
        for name in available_models:
            if "flash" in name.lower():
                return name
        
        # If no flash, return the first available one
        return available_models[0]
    except Exception as e:
        st.error(f"Failed to fetch models: {e}")
        return "models/gemini-1.5-flash" # Hardcoded fallback

working_model_name = get_best_model()
st.caption(f"Connected to: `{working_model_name}`")

# --- 3. CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- 4. CHAT LOGIC ---
if prompt := st.chat_input("Ask me anything..."):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        try:
            model = genai.GenerativeModel(working_model_name)
            # stream=True makes it feel interactive
            response = model.generate_content(prompt, stream=True)
            
            full_res = ""
            placeholder = st.empty()
            
            for chunk in response:
                full_res += chunk.text
                placeholder.markdown(full_res + "▌")
            
            placeholder.markdown(full_res)
            st.session_state.messages.append({"role": "assistant", "content": full_res})
            
        except Exception as e:
            st.error(f"API Error: {e}")
