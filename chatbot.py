import streamlit as st
import openai

st.title("ChatGPT-like clone")

# Set OpenAI API key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Allow user to select the model
model_options = ["gpt-2", "gpt-3.5-turbo", "gpt-4"]
selected_model = st.selectbox("Choose the model", model_options)

# Set the selected model in session state
st.session_state["openai_model"] = selected_model

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Get response from OpenAI API and display it
    with st.spinner(text="Assistant is thinking..."):
        response = openai.ChatCompletion.create(
            model=st.session_state["openai_model"],
            messages=[{"role": "user", "content": m["content"]} for m in st.session_state.messages],
            max_tokens=150,
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0,
            stop=["\n"],
            n=1
        )
        # Extract completion text from the response object
        completion_text = response.choices[0].message["content"]
        
        # Display completion text in the chat message container
        with st.chat_message("assistant"):
            st.markdown(completion_text)
        
        # Add completion text to chat history
        st.session_state.messages.append({"role": "assistant", "content": completion_text})
