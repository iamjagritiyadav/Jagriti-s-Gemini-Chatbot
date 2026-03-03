# Streamlit Gemini Chatbot

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-ff4b4b)
![Google Gemini](https://img.shields.io/badge/LLM-Gemini-green)

---

## Overview

This project is a lightweight AI chatbot built using Streamlit and Google Gemini.

It provides a clean chat interface, dynamic model selection, streaming responses, and session-based chat history management.

The application automatically detects and prioritizes fast Gemini "Flash" models when available, ensuring optimal performance.

---

## Features

* Secure API key management using Streamlit Secrets
* Dynamic model detection from available Gemini models
* Automatic prioritization of Flash models for speed
* Streaming response generation
* Persistent chat history using session state
* Clean, minimal user interface
* Graceful error handling

---

## Architecture

### 1. Secure Configuration

The Gemini API key is loaded securely from `st.secrets`.

If the key is missing, the application stops execution and displays an error message.

### 2. Dynamic Model Selection

The system:

* Fetches all available Gemini models
* Filters models that support `generateContent`
* Prioritizes models containing "flash"
* Falls back to `gemini-1.5-flash` if necessary

The selected model is cached using `@st.cache_resource` to avoid repeated API calls.

### 3. Chat State Management

Conversation history is stored in `st.session_state.messages`.

This allows:

* Persistent messages during session
* Structured role-based message storage (user / assistant)

### 4. Streaming Response Logic

Responses are streamed token-by-token.

A placeholder element updates dynamically to create a cursor-style typing effect.

---

## Project Structure

```
├── app.py          # Main Streamlit chatbot application
├── .streamlit/
│   └── secrets.toml  # Stores GEMINI_API_KEY securely
└── requirements.txt  # Project dependencies
```

---

## Installation & Setup

### 1. Clone the Repository

```
git clone <your-repo-url>
cd <repo-name>
```

---

### 2. Install Dependencies

Create a virtual environment and install required packages:

```
pip install -r requirements.txt
```

Example `requirements.txt`:

```
streamlit
google-generativeai
```

---

### 3. Configure API Key

Create a folder named `.streamlit` in the root directory.

Inside it, create a file named `secrets.toml`:

```
GEMINI_API_KEY = "your_google_ai_studio_api_key"
```

---

### 4. Run the Application

```
streamlit run app.py
```

The application will start locally and open in your browser.

---

## How It Works

1. User enters a prompt.
2. The system appends the message to session state.
3. Gemini model generates a streaming response.
4. The UI updates live with a typing effect.
5. Final response is stored in chat history.

---

## Error Handling

* Stops execution if API key is missing.
* Displays model-fetch failure messages.
* Handles runtime errors during generation.

---

## Future Improvements

* Multi-turn conversational memory using structured prompts
* System role injection for personality control
* Conversation export feature
* Deployment on Streamlit Cloud
* Token usage tracking
* Rate limit monitoring

---

## License

This project is licensed under the MIT License.

---

This project demonstrates secure API usage, streaming LLM integration, and stateful UI design using Streamlit.
