import streamlit as st
import google.generativeai as genai

# --- PAGE CONFIG ---
st.set_page_config(page_title="JAGRITI'S CHATBOT", page_icon="✨", layout="centered")

# --- CUSTOM CSS (The "Gemini" Look) ---
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #131314;
        color: #e3e3e3;
    }
    /* Style Chat Input */
    .stChatInput {
        bottom: 20px;
    }
    /* Rounded corners for chat bubbles */
    [data-testid="stChatMessage"] {
        background-color: #1e1f20;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 10px;
    }
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #1e1f20;
    }
    </style>
    """, unsafe_allow_html=True)

# --- API SETUP ---
# Fetching from Streamlit Secrets (as you mentioned you already have this)
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
except Exception as e:
    st.error("API Key not found in Streamlit Secrets!")

model = genai.GenerativeModel("gemini-1.5-flash")

# --- CHAT HISTORY INITIALIZATION ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_session" not in st.session_state:
    # This starts the Gemini-native history tracking
    st.session_state.chat_session = model.start_chat(history=[])

# --- SIDEBAR (History/Settings) ---
with st.sidebar:
    st.title("✨ Gemini Chat")
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.chat_session = model.start_chat(history=[])
        st.rerun()
    st.info("Ask anything! This bot remembers the conversation.")

# --- DISPLAY CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar="👤" if message["role"] == "user" else "✨"):
        st.markdown(message["content"])

# --- CHAT INPUT ---
if prompt := st.chat_input("Ask Gemini..."):
    # 1. Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    # 2. Save to history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 3. Generate response
    with st.chat_message("assistant", avatar="✨"):
        message_placeholder = st.empty()
        full_response = ""
        
        try:
            # Using stream=True makes it feel much more like Gemini
            response = st.session_state.chat_session.send_message(prompt, stream=True)
            for chunk in response:
                full_response += chunk.text
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    # 4. Save assistant response to history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
