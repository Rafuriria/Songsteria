#this is version 1.0


import streamlit as st
import random
import collections.abc
collections.Hashable = collections.abc.Hashable
import yaml

# Specify the full path to the YAML file
file_path = r'C:\Users\User\Desktop\SONGSTERIA\pages\depression.yml'

def load_dataset(file_path):
    with open(file_path, "r") as file:
        dataset = yaml.safe_load(file)
    return dataset.get("conversations", [])

def get_chatbot_response(user_input, dataset, conversation_history):
    for conversation in dataset:
        if user_input in conversation:
            responses = conversation[conversation.index(user_input) + 1]

            # Randomly select one response
            selected_response = random.choice(responses)

            # Include the entire conversation in the responses
            full_responses = conversation_history.copy()
            full_responses.append({"user": user_input, "bot": selected_response})

            return full_responses

def main():
    st.title("AidBot")

    dataset = load_dataset(file_path)
    conversation_history = st.session_state.get("conversation_history", [])

    # Display the entire conversation as a chatbox
    st.markdown('<style>div.Widget.row-widget.stButton > div{flex-direction: column;}</style>', unsafe_allow_html=True)
    for entry in conversation_history:
        if entry['user']:
            st.markdown(f'<div style="display: flex; justify-content: flex-end; padding: 5px;"><div style="background-color: #DA70D6; color: #fff; padding: 10px; border-radius: 10px; margin: 5px; max-width: 70%;">{entry["user"]}</div></div>', unsafe_allow_html=True)
        if entry['bot']:
            st.markdown(f'<div style="display: flex; padding: 5px;"><div style="background-color: #a2d5f2; color: #1f1f1f; padding: 10px; border-radius: 10px; margin: 5px; max-width: 70%;">{entry["bot"]}</div></div>', unsafe_allow_html=True)

    # User input field under the chat history
    user_input = st.text_input("You:")

    response_button = st.button("Get Response")

    if user_input and response_button:
        bot_responses = get_chatbot_response(user_input, dataset, conversation_history)

        # Save conversation history to session state
        st.session_state.conversation_history = bot_responses

if __name__ == "__main__":
    main()
