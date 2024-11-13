from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os
import json
from langchain_mongodb import MongoDBAtlasVectorSearch
from pymongo import MongoClient
from uuid import uuid4

# load .env file
load_dotenv()

with open("./config.json") as f:
    config = json.load(f)

client = MongoClient(os.getenv("CONNECTION_STRING"))
DB_NAME = "langchain_test_db"
COLLECTION_NAME = "langchain_test_vectorstores"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "langchain-test-index-vectorstores"
MONGODB_COLLECTION = client[DB_NAME][COLLECTION_NAME]


# def get_vector_store(collection_name):

#     vector_store = Chroma(
#          collection_name,
#          embedding_function= GoogleGenerativeAIEmbeddings(
#              model=config["vector_db"]["embedding_model"],
#              google_api_key=os.getenv("GOOGLE_API_KEY")
#          ),
#         persist_directory=config["vector_db"]["persist_directory"]
#      )
#     return vector_store

def get_vector_store():

    vector_store = MongoDBAtlasVectorSearch(
        collection=MONGODB_COLLECTION,
        embedding= GoogleGenerativeAIEmbeddings(
            model=config["vector_db"]["embedding_model"],
            google_api_key=os.getenv("GOOGLE_API_KEY")
        ),
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
        relevance_score_fn="cosine",
    )
    

    
    return vector_store
  


def add_to_vector_store(docs, vector_store):
      print("Adding docs to vector store ...")
      uuids = [str(uuid4()) for _ in range(len(docs))]
      vector_store.add_documents(documents=docs, ids=uuids)
      print(f"Documents successfully added to collection")

   
       
