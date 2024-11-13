

import os

def get_files_list(directory, file_type=".pdf"):
  return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith(file_type)]


def load_processed_files(processed_files_path):
    # Check if the file exists; if not, return an empty list
    if os.path.exists(processed_files_path):
        with open(processed_files_path, 'r') as file:
            return file.read().splitlines()
    return []


def save_processed_file(file_name, processed_files_path):
    # Append the file name to the processed files list
    with open(processed_files_path, 'a') as file:
        file.write(file_name + '\n')
    print(f"Saved file {file_name}")    
