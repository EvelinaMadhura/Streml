import streamlit as st
import replicate

# Set your Replicate API token
REPLICATE_API_TOKEN = ""

# Initialize the Replicate client
client = replicate.Client(api_token=REPLICATE_API_TOKEN)

# Function to generate text with Replicate
def generate_text(prompt, max_length=100, top_k=5, num_return_sequences=1):
    model_version = "joehoover/falcon-40b-instruct:7d58d6bddc53c23fa451c403b2b5373b1e0fa094e4e0d1b98c3d02931aa07173"
    parameters = {
        "prompt": prompt,
        "max_length": max_length,
        "top_k": top_k,
        "num_return_sequences": num_return_sequences,
    }
    
    try:
        output_generator = client.run(model_version, input=parameters)
        
        generated_texts = []
        current_text = ""
        
        for output in output_generator:
            st.write("Debug: Received output from generator")  # Debug line
            st.write(output)  # Debug line
            if 'generated_text' in output:
                current_text += output['generated_text']
        
        if current_text:
            generated_texts.append(current_text)
        
        if not generated_texts:
            return ["Sorry, I couldn't generate a response for that input."]
        
        return generated_texts

    except Exception as e:
        st.write(f"Debug: An error occurred - {e}")  # Debug line
        return [f"An error occurred: {e}"]

# Streamlit app
st.title("ChatFalcon-like App with Falcon 7B")

if "messages" not in st.session_state:
    st.session_state.messages = []

for i, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"], key=f"message_{i}"):
        st.markdown(message["content"])

if prompt := st.chat_input("What is up?", key="user_input"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    generated_texts = generate_text(prompt)
    if generated_texts:
        for i, generated_text in enumerate(generated_texts, start=1):
            with st.chat_message("assistant"):
                st.markdown(generated_text)
                st.session_state.messages.append({"role": "assistant", "content": generated_text})
    else:
        with st.chat_message("assistant"):
            st.markdown("Sorry, I couldn't generate a response for that input.")
            st.session_state.messages.append({"role": "assistant", "content": "Sorry, I couldn't generate a response for that input."})

