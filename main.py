from utils.file_func import get_files_list, load_processed_files, save_processed_file
from utils.doc_func import load_docs_from_pdf_files, split_docs
from utils.vector_store import add_to_vector_store
import json
from utils.vector_store import add_to_vector_store, get_vector_store
from utils.retriver import get_retriever
from utils.chains import get_history_aware_retriever, get_rag_chain, conversational_rag_chain
import streamlit as st
import uuid

def main():
  try:
    with open("./config.json") as f:
      config = json.load(f)
    
    stored_pdf_files_directory = config["stored_pdf_files_directory"]
    collection_name = config["vector_db"]["collection_name"]
    processed_files_path = config["processed_files_path"]
    vector_store_pdf = get_vector_store(collection_name)

    for file in get_files_list(directory= stored_pdf_files_directory):
      processed_files = load_processed_files(processed_files_path)

      if file not in processed_files:
        print(f"Processing file: {file}")
        docs = load_docs_from_pdf_files(file)
        splits = split_docs(docs)
        add_to_vector_store(splits, vector_store_pdf)
        save_processed_file(file, processed_files_path)
  
    if "conversation_rag_chain" not in st.session_state:
     
      retriever_pdf = get_retriever(search_type="similarity", vector_store= vector_store_pdf, k = 5)
      history_aware_retriver = get_history_aware_retriever(retriever_pdf)
      rag_chain = get_rag_chain(history_aware_retriver)
      conversation_rag_chain = conversational_rag_chain(rag_chain)
      st.session_state.conversation_rag_chain = conversation_rag_chain

    conversation_rag_chain = st.session_state.conversation_rag_chain
    
    st.set_page_config(
        page_title="Software Process Guide AI",
        page_icon="💻",
        layout="centered",
        initial_sidebar_state="expanded"
    )

    # Main header for the application
    st.header('Software Process Guide AI 💻 🧠')

    # Subheader explaining the tool's purpose
    st.subheader(
        'Your AI Assistant for Navigating Software Development Processes 🛠️')

    # Information or instructions section
    st.markdown("""
    Welcome to the **Software Process Guide AI**! This tool leverages a pre-trained generative AI model to assist you through each phase of the software development lifecycle, specifically designed for the **Scrum framework**.
    """)
    
    # initialize chat history
    if "messages" not in st.session_state:
      st.session_state.messages = []
    # generate session id for the chat  
    if "session_id" not in st.session_state:
      st.session_state.session_id = str(uuid.uuid4())
      #  st.session_state.session_id = "fsdfdfs"

    with st.sidebar:
      session_id_container = st.empty()
      # Display the session ID
      session_id_container.write(
        f"**Session ID:** {st.session_state['session_id']}")

      # Add a button to start a new chat
      if st.button("New Chat"):
          # Reset chat history and generate a new session ID
          st.session_state.messages = []
          st.session_state.session_id = str(uuid.uuid4())
          session_id_container.write(
              f"**Session ID:** {st.session_state['session_id']}")
          st.success("New chat started!")
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
      with st.chat_message(message["role"]):
          st.markdown(message["content"])

    if prompt := st.chat_input("Message ..."):
      # Add user message to chat history
      st.session_state.messages.append({"role": "user", "content": prompt})
      # Display user message in chat message container
    
      with st.chat_message("user"):
        st.markdown(prompt)

      typing_indicator = st.empty()  
      typing_indicator.write("AI is processiong your request...")

  
      response = conversation_rag_chain.invoke(
          {
              "input": prompt
          },
          config={
              "configurable": {"session_id": st.session_state.session_id}
            },
        )
      

      typing_indicator.empty()  # Remove the typing indicator when done

      with st.chat_message("ai"):
          # display the AI's answer
          st.markdown(response)

          st.session_state.messages.append(
                {"role": "ai", "content": response})


  except Exception as e:
    if typing_indicator:
      typing_indicator.empty()  # Remove the typing indicator when done
    st.error("An error occurred while processing request")   

    print(f"An error occurred {e}")

if __name__ == "__main__":
    main()
  




