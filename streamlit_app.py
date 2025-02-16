import streamlit as st
import time
from openai import OpenAI

# Show title and description
st.title("💬 Chatbot")
st.write(
    "This is a simple chatbot that uses OpenAI's GPT-3.5 model to generate responses. "
    "To use this app, you need to provide an OpenAI API key, which you can get [here](https://platform.openai.com/account/api-keys). "
)

# Ask for OpenAI API Key
openai_api_key = st.text_input("OpenAI API Key", type="password")

# Ensure the user enters an API key
if not openai_api_key:
    st.info("🗝️ Please enter your OpenAI API key to continue.")
else:
    # Create OpenAI client
    client = OpenAI(api_key=openai_api_key)

    # Store chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input field
    if prompt := st.chat_input("What is up?"):
        # Store & Display user input
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Add a delay to avoid hitting the rate limit
        time.sleep(1)

        try:
            # Generate response using OpenAI API
            stream = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            )

            # Display response in real-time
            with st.chat_message("assistant"):
                response_text = ""
                for chunk in stream:
                    response_text += chunk.choices[0].delta.get("content", "")

                st.markdown(response_text)

            # Store response in chat history
            st.session_state.messages.append({"role": "assistant", "content": response_text})

        except Exception as e:
            st.error(f"⚠️ OpenAI API Error: {str(e)}")
