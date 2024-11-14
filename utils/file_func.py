

import os
from pymongo import MongoClient
from dotenv import load_dotenv
import json

load_dotenv()

with open("./config.json") as f:
    config = json.load(f)

client = MongoClient(os.getenv("CONNECTION_STRING"))
db = client[config["history_db"]["database_name"]]
collection = db["file_names"]


def get_files_list(directory, file_type=".pdf"):
  return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(file_type)]


def load_processed_files():
    # Retrieve already processed file names from the database
    processed_files = collection.find({}, {"_id": 0, "file_name": 1})
    return [file["file_name"] for file in processed_files]

  
def save_processed_file(file_name, file_type):
    # Insert the file name and type into MongoDB if it's not already processed
    if collection.find_one({"file_name": file_name}) is None:
        collection.insert_one({"file_name": file_name, "file_type": file_type})
        print(f"Saved file {file_name} of type {file_type}")


# def load_processed_files(processed_files_path):
#     # Check if the file exists; if not, return an empty list
#     if os.path.exists(processed_files_path):
#         with open(processed_files_path, 'r') as file:
#             return file.read().splitlines()
#     return []
# def save_processed_file(file_name, processed_files_path):
#     # Append the file name to the processed files list
#     with open(processed_files_path, 'a') as file:
#         file.write(file_name + '\n')
#     print(f"Saved file {file_name}")
# Function to load already processed files from MongoDB
