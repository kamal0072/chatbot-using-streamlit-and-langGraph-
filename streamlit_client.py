import streamlit as st
from langGraph_tools import chatbot, retrieve_all_threads
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
import uuid

# **************************************** utility functions *************************
def generate_thread_id():
    thread_id = uuid.uuid4()
    return thread_id


def reset_chat():
    thread_id = generate_thread_id()
    st.session_state['thread_id'] = thread_id
    add_thread(st.session_state['thread_id'])
    st.session_state['message_history'] = []


def add_thread(thread_id):
    if thread_id not in st.session_state['chat_threads']:
        st.session_state['chat_threads'].append(thread_id)


def load_conversation(thread_id):
    state = chatbot.get_state(
        config={'configurable': {'thread_id': thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return state.values.get('messages', [])


st.set_page_config(
    page_title="Chatbot for a change",
    page_icon="🤖",
    layout="wide",
)
st.title("Chatbot like chatGpt")

# **************************************** Session Setup ******************************
if 'message_history' not in st.session_state:
    st.session_state['message_history'] = []

if 'thread_id' not in st.session_state:
    st.session_state['thread_id'] = generate_thread_id()

if 'chat_threads' not in st.session_state:
    st.session_state['chat_threads'] = retrieve_all_threads()
add_thread(st.session_state['thread_id'])


# **************************************** Sidebar UI *********************************
st.sidebar.title("Chatbot for a change")
if st.sidebar.button("New Chat Session"):
    reset_chat()
st.sidebar.header("My chat history")

for thread_id in st.session_state['chat_threads'][::-1]:
    if st.sidebar.button(str(thread_id)):
        print("The thread id is + ", thread_id)
        st.session_state['thread_id'] = thread_id
        messages = load_conversation(thread_id)

        temp_messages = []

        for msg in messages:
            if isinstance(msg, HumanMessage):
                role = 'user'
            else:
                role = 'assistant'
            temp_messages.append({'role': role, 'content': msg.content})

        st.session_state['message_history'] = temp_messages


# # **************************************** Main UI ************************************
# loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input(placeholder="Type your message here...")
if user_input:
    # first add the messags to messages history
    st.session_state['message_history'].append(
        {'role': 'user', 'content': user_input})
    with st.chat_message('user', avatar="https://i.pravatar.cc/150?u=a042581f4e28540bc8c1"):
        st.text(user_input)

    # CONFIG = {"configurable" : {'thread_id' : st.session_state['thread_id']}}

    CONFIG = {
        "configurable": {'thread_id': st.session_state['thread_id']},
        "metadata" : {
            'thread_id' : st.session_state['thread_id']
        },
        "run_name" : "Chatbot With UI"
    }

    # first add the message to message_history
    with st.chat_message('assistant', avatar="https://i.pravatar.cc/150?u=a042581f4e28540bc8c2"):
        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages"
            ):
                if isinstance(message_chunk, AIMessage):
                    # yield only assistant tokens
                    yield message_chunk.content
        ai_message = st.write_stream(ai_only_stream)
    st.session_state['message_history'].append(
        {'role': 'assistant', 'content': ai_message}, )
