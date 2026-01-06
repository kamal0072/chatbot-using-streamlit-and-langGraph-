# from langchain_huggingface import HuggingFaceEndpointEmbeddings
# from langchain_classic.schema import Document
# from langchain_classic.retrievers.contextual_compression import ContextualCompressionRetriever
# from langchain_classic.retrievers.document_compressors import LLMChainExtractor
# from langchain_core.documents import Document

# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda
# from langchain_core.prompts import PromptTemplate
# from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace, HuggingFaceEndpointEmbeddings
# from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
# from langchain_classic.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import FAISS
# try:
#     video_id = "Gfr50f6ZBvo"    # only the ID, not full URL/transcript not found for this will show error
#     # video_id = "Gfr50f6ZBvo"
#     # If you don’t care which language, this returns the “best” one
#     api = YouTubeTranscriptApi()
#     transcript = api.fetch(video_id=video_id, languages=['en', 'hi'])
#     transcript_list = transcript.snippets
#     transcript_list = [transcript_list[i].text for i in range(len(transcript_list))]
#     lis = " ".join(transcript_list)

#     splitter =  RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
#     chunks = splitter.create_documents([lis])
#     # print(chunks[100])
#     # print(len(chunks))
#     embeddings = HuggingFaceEndpointEmbeddings( )
#     vector_store = FAISS.from_documents(
#         documents=chunks,
#         embedding=embeddings
#     )
#     # print(vector_store.index_to_docstore_id)
#     # print(vector_store.get_by_ids(['3d495d0a-3f66-4742-86f7-626845e22f7e']))

#     llm=HuggingFaceEndpoint(
#         repo_id="meta-llama/Llama-3.2-3B-Instruct",
#         task="text-generation",
#         max_new_tokens=100,
#         temperature=0.3
#     )
#     prompt = PromptTemplate(
#         template="""      You are a helpful assistant.
#       Answer ONLY from the provided transcript context.
#       If the context is insufficient, just say you don't know.

#     {context}
#     Question: {question}""",
#     input_variables=["context", "question"]
#     )
#     retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 2})
#     question = "What is the meaning of life?"

#     retrieved_docs = retriever.invoke(question)

#     def format_docs(retrieved_docs):
#         context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
#         return context_text
#     parallel_chain = RunnableParallel({
#         'context': retriever | RunnableLambda(format_docs),
#         'question': RunnablePassthrough()
#     })
#     parser = StrOutputParser()
#     main_chain = parallel_chain | prompt | llm | parser
#     print(main_chain.invoke("can you summary this video in 2-3 sentences?"))


from langchain_huggingface import HuggingFaceEndpoint, ChatHuggingFace
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages

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

# checkpointer
checkpointer = InMemorySaver()

# creating graph
graph = StateGraph(ChatState)

graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

# chatbot
chatbot = graph.compile(checkpointer = checkpointer)