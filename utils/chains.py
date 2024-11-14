import os
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import GoogleGenerativeAI
from dotenv import load_dotenv
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_mongodb.chat_message_histories import MongoDBChatMessageHistory
import json
from operator import itemgetter
from langchain_groq import ChatGroq
load_dotenv()

with open("./config.json") as f:
  config = json.load(f)



def get_history_aware_retriever(retriever):
  # retriever = get_retriever(collection_name)
  llm = GoogleGenerativeAI(
      model=config["history_aware_retriever"]["model"], 
      temperature=config["history_aware_retriever"]["tempreture"], api_key=os.getenv("GOOGLE_API_KEY"))

  contextualize_q_system_prompt = """
  Given a chat history and the latest user question 
  which might reference context in the chat history, formulate a standalone question 
  which can be understood without the chat history. Do NOT answer the question, 
  just reformulate it if needed and otherwise return it as is.
  """

  prompt_genrate_q = ChatPromptTemplate.from_messages(
      [
          ("system", contextualize_q_system_prompt),
          MessagesPlaceholder("chat_history"),
          ("human", "{input}"),
      ]

  )

  my_history_aware_retriever = prompt_genrate_q | llm | StrOutputParser() | retriever
  return my_history_aware_retriever




def get_rag_chain(my_history_aware_retriever):
  
  # qa_system_prompt = """
  # You are a software process assistant specializing in Agile methodologies.
  # Use the following pieces of provided context along with the conversation history to answer questions related to Agile process activities, 
  # best practices, and guidelines.
  # The context will contain guildelines and agile development principles.
  # Use these when formulating your answer to questions.

  # If the context does not provide sufficient information, you may rely on your own knowledge to generate a helpful response.
  # If you still don't know the answer, clearly state that you do not have that information.
  

  # Chat History: {chat_history}
  # Context: {context}
  # """
  # qa_system_prompt = """
  # You are a software process assistant specializing in Agile methodologies.
  # Use the following pieces of provided context, which will contain guidelines
  # and Agile development principles, along with the conversation history to
  # answer questions related to Agile process activities, best practices, and guidelines.
  # Prioritize any Scrum framework practices and address Agile activities 
  # like Sprint Planning, Daily Stand-ups, Retrospectives, and Backlog Refinement where applicable.
  # If the context does not provide sufficient information, you may rely on your own knowledge
  # to generate a helpful response. If you still don't know the answer, clearly state that 
  # you do not have that information

  # Chat History: {chat_history}
  # Context: {context}
  # """
  qa_system_prompt = """
  You are a software process assistant specializing in the Scrum framework, which is one of the most widely used Agile frameworks.
  Use the following pieces of provided context along with the conversation history to answer questions related to Scrum activities,
  best practices, and guidelines.
  If the context does not provide sufficient information, you may rely on your own knowledge to generate a helpful response.
  If you still don't know the answer, clearly state that you do not have that information.
  
  Chat History: {chat_history}
  Context: {context}
  """

#   llm = GoogleGenerativeAI(model="gemini-1.5-flash",
#                            temperature=1,
#                            api_key=os.getenv("GOOGLE_API_KEY"))
  llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"),
                 model="llama-3.1-8b-instant")

  qa_prompt = ChatPromptTemplate.from_messages(
      [
          ("system", qa_system_prompt),
          ("human", "{input}"),
      ]
  )

  
  rag_chain = (
      {"context": my_history_aware_retriever, "chat_history": itemgetter("chat_history"), "input": itemgetter("input")} |
      qa_prompt |
      llm |
      StrOutputParser()
      
  )
  return rag_chain


def conversational_rag_chain(rag_chain):
  
  def load_history_with_debug(session_id):
      # Load the chat history from MongoDB
      chat_message_history = MongoDBChatMessageHistory(
          session_id=session_id,
          connection_string=os.getenv("CONNECTION_STRING"),
          database_name=config["history_db"]["database_name"],
          collection_name=config["history_db"]["collection_name"],
          create_index= True,
         
      )
    #   history = chat_message_history
      
    #   history.messages = history.messages[-2:]
    #   history.
    #   print(chat_message_history.messages)
    #   print(len(chat_message_history.messages))
    #   print(chat_message_history.history_size)
      
      return chat_message_history

  conversational_rag_chain = RunnableWithMessageHistory(
      rag_chain,
    get_session_history= load_history_with_debug,
      input_messages_key="input",
      history_messages_key="chat_history"
  )
  return conversational_rag_chain
