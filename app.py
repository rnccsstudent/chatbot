import streamlit as st
import google.generativeai as genai

# Set up the Gemini API Key
st.title("💬 Chatbot with Google Gemini")
st.write(
    "This chatbot uses Google's Gemini API to generate responses. "
    "To use this app, you need to provide a Google Gemini API key, which you can get [here](https://aistudio.google.com/)."
)

# Ask user for their API key
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

        # Store and display the user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Send request to Gemini API
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)

        # Display response
        if response.text:
            bot_reply = response.text
        else:
            bot_reply = "⚠️ Sorry, I couldn't generate a response."

        with st.chat_message("assistant"):
            st.markdown(bot_reply)

        # Store bot reply in session
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
