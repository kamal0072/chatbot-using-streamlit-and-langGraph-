import streamlit as st
from messages import chatbot
from langchain_core.messages import BaseMessage, HumanMessage

st.set_page_config(
    page_title="Chatbot for a change",
    page_icon="🤖",
    layout="wide",
)

# navibation bar
st.markdown("""
        <style>
        .navbar {
            overflow: hidden;
            background-color: #333a00;
        }

        .navbar a {
            float: left;
            font-size: 16px;
            color: white;
            text-align: center;
            padding: 14px 16px;
            text-decoration: none;
        }
        .navbar a:hover {
            background-color: #ddd;
            color: black;
        }    
        </style>            
        <div class="navbar">
            <a href="#">Home</a>
            <a href="#">Analytics</a>
            <a href="#">Settings</a>
            <a href="#">Help</a>
            <a href="#">Find on Github</a>
            <a href="#">Contact</a>
        </div>

        <div class="spacer"></div>
""", unsafe_allow_html=True)

# ---------------------------------
# Sidebar
# ---------------------------------
with st.sidebar:
    st.title("⚙️ Chatbot Settings")
    st.markdown("---")
    st.info(
        "Choose your options for the conversation."
    )
# sidebar options with dropdown menu bar
enable_menu = st.sidebar.toggle("Show Menu", value=True)
if enable_menu:
    with st.sidebar.expander("🏠 Home"):
        st.button("Dashboard")
        st.button("Overview")

    with st.sidebar.expander(" 🎓 Education"):
        st.button("Technical")
        st.button("Non-Technical")
        st.button("General")
        st.button("Other")
        st.button("Resume")
        st.button("Cover Letter")

    with st.sidebar.expander(" 🚨 Health & Safety"):
        st.button("Fever")
        st.button("Cough")
        st.button("Tiredness")
        st.button("Fatigue")
        st.button("Sore Throat")
        st.button("Headache")
        st.button("Nausea")
    with st.sidebar.expander("🌾 Agriculture"):
        st.button("Cultivation")
        st.button("Soil")
        st.button("Fertilizer")
        st.button("Pesticides")
        st.button("Irrigation")
    with st.sidebar.expander(" 🌍 Social awareness"):
        st.button("Social Media")
        st.button("Cyberbullying")
        st.button("Harassment")
        st.button("Rape and Abuse")
else:
    st.sidebar.warning("Menu is hidden")
st.title("Chatbot for a change")

CONFIG1 = {"configurable" : {'thread_id' : "thread-1"}}
# creating a chat history
if 'message_history' not in st.session_state:
    st.session_state.message_history = []

# loading the conversation history
for msg in st.session_state.message_history:
    with st.chat_message(msg['role']):
        st.text(msg['content'])

user_input = st.chat_input(placeholder="Type your message here...")
if user_input:
    # first add the messags to messages history
    st.session_state.message_history.append({'role': 'user', 'content': user_input})
    with st.chat_message('user', avatar="https://i.pravatar.cc/150?u=a042581f4e28540bc8c1"):
        st.write(user_input)

    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=CONFIG1)
    ai_message = response['messages'][-1].content
    # first add the messags to messages history
    st.session_state.message_history.append({'role': 'assistant', 'content': ai_message}, )
    with st.chat_message('assistant', avatar="https://i.pravatar.cc/150?u=a042581f4e28540bc8c2"):
        st.text(ai_message)
