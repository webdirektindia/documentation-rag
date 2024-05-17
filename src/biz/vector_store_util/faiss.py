from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

import os
import streamlit as st

# Directory for storing FAISS vector data
__faiss_vector_store_directory = os.environ.get('faiss_vector_store_directory')  
__embedding_model = os.environ["OPENAI_API_EMBEGGING_MODEL"]

def save_faiss_vector_db(store_name: str, chunks) -> bool:
    """
    Save document chunks into a FAISS vector database.

    Args:
    - store_name (str): Name of the store/database.
    - chunks (list): List of document chunks to store.

    Returns:
    - None
    """
    result = False
    try:
        if chunks:
            # Construct the path for storing the vector database
            store_path = os.path.join(__faiss_vector_store_directory, store_name) 
            print(f'>>> storing chunks to path {store_path}.')
            # Check if the vector store already exists
            if not os.path.exists(store_path):
                embedding = OpenAIEmbeddings(model=__embedding_model)
                # Create and save the vector database
                vector_db = FAISS.from_texts(chunks, embedding=embedding)
                vector_db.save_local(store_path)
                
                result = True
            else:
                print(f"Vector store '{store_name}' already exists.")
    except Exception as e:
        # Handle other exceptions
        print(f"Error saving FAISS vector database: {e}")
    
    return result

def get_faiss_vector_db():
    """
    Load the FAISS vector database.

    Returns:
    - FAISS vector database if successful, None otherwise.
    """
    try:
        # Check if the vector directory exists 
        if os.path.exists(__faiss_vector_store_directory):
            # Get a list of files in the vector directory
            dir_files = os.listdir(__faiss_vector_store_directory)
            
            if dir_files:
                # Load the FAISS vector database
                vector_db = load_faiss_vector_database(dir_files)
                return vector_db
            else:
                print("No files found in the vector store directory.")
        else:
            print("Vector store directory does not exist.")
    except Exception as e:
        # Handle other exceptions
        print(f"Error loading FAISS vector database: {e}")
        return None

def load_faiss_vector_database(dir_files):
    """
    Load FAISS vector database from files.

    Args:
    - dir_files (list): List of files in the vector directory.

    Returns:
    - FAISS vector database if successful, None otherwise.
    """
    try:
        # Initialize an empty vector database
        vector_db = None
        
        # Loop through each file in the directory
        for dir_file in dir_files:
            # Construct the full path to the file
            store_path  = os.path.join(__faiss_vector_store_directory, dir_file)
            # Check if the file is a FAISS vector database
            if os.path.exists(store_path):                
                # Load the vector database
                if vector_db is None:
                    vector_db = FAISS.load_local(
                        store_path, 
                        OpenAIEmbeddings(model=__embedding_model),
                        allow_dangerous_deserialization=True
                    )
                else:
                    # Load another vector database and merge
                    load_vector_db = FAISS.load_local(
                        store_path, 
                        OpenAIEmbeddings(model=__embedding_model),
                        allow_dangerous_deserialization=True
                    )
                    vector_db.merge_from(load_vector_db)
            else:
                print(f"Store '{dir_file}' is not a FAISS vector database.")
        
        return vector_db
    except Exception as e:
        # Handle unexpected exceptions
        print(f"Error loading FAISS vector database: {e}")
        return None