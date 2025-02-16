import streamlit as st
import google.generativeai as genai

# Streamlit UI
st.title("💬 Chatbot with Google Gemini")
st.write(
    "This chatbot uses Google's Gemini API to generate responses. "
    "To use this app, you need to provide a Google Gemini API key, which you can get [here](https://aistudio.google.com/)."
)

# Ask user for their Gemini API key
gemini_api_key = st.text_input("Google Gemini API Key", type="password")

if not gemini_api_key:
    st.info("Please add your Google Gemini API key to continue.", icon="🗝️")
else:
    # Configure Gemini API
    genai.configure(api_key=gemini_api_key)

    # Create a session state variable to store messages
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display existing chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me anything..."):

        # Store and display user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response from Gemini API
        model = genai.GenerativeModel("gemini-pro")

        try:
            response = model.generate_content(prompt)
            bot_reply = response.text if hasattr(response, "text") else "⚠️ Sorry, I couldn't generate a response."

        except Exception as e:
            bot_reply = f"⚠️ Error: {str(e)}"

        # Display response
        with st.chat_message("assistant"):
            st.markdown(bot_reply)

        # Store bot reply in session
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
