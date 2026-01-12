from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
import dotenv
import os

dotenv.load_dotenv()
# checking langghain api key
# print(os.getenv("LANGCHAIN_API_KEY"))
# make llm
model = ChatHuggingFace(
    llm=HuggingFaceEndpoint(
        repo_id="meta-llama/Llama-3.2-3B-Instruct",
        task="text-generation",
        max_new_tokens=100,
    )
)

# define state for a chat session
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


# make nodes
def chat_node(state: ChatState) -> ChatState:
    messages = state["messages"]
    response = model.invoke(messages)
    return {'messages' : [response]}

# create database
conn = sqlite3.connect(database='chatbotData.db', check_same_thread=False) #
# checkpointer
# checkpointer = InMemorySaver()
checkpointer = SqliteSaver(conn=conn)

# creating graph
graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

# chatbot
chatbot = graph.compile(checkpointer = checkpointer)

# checkpointer = checkpointer.list()
# print("checkpointer generater :- ", checkpointer)
# print(len(checkpointer))
def retrive_all_thread():
    all_set = set()
    for checkpoint in checkpointer.list(None):
        # print(checkpoint)
        # print(checkpoint.config)
        # print(checkpoint.config["configurable"]["thread_id"])
        all_set.add(checkpoint.config["configurable"]["thread_id"])
    return list(all_set)
