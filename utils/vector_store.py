from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
import json
# load .env file
load_dotenv()

with open("./config.json") as f:
    config = json.load(f)

def get_vector_store(collection_name):

    vector_store = Chroma(
         collection_name,
         embedding_function= GoogleGenerativeAIEmbeddings(
             model=config["vector_db"]["embedding_model"],
             google_api_key=os.getenv("GOOGLE_API_KEY")
         ),
        persist_directory=config["vector_db"]["persist_directory"]
     )
    return vector_store
  


def add_to_vector_store(docs, vector_store):
      print("Adding docs to vector store ...")
      vector_store.add_documents(docs)
      print(f"Documents successfully added to collection")

   
       
