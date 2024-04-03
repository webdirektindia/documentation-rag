from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFMinerLoader
from langchain_community.vectorstores import FAISS
from transformers import AutoModelForCausalLM, AutoTokenizer

import streamlit as st
import os as os

# import local class file
from model.vector import vector_db
from model.upload_file import upload_file

class pdf_embeddings:   
    __directory = r"./data/"
    
    # Instance attribute 
    def __init__(self, name): 
        self.name = name        
        load_dotenv() # read local .env file
         
    def generate_pdf_embeddings(self, pdfs):
        # if file is selected
        if pdfs is not None:
            # instance of the class
            obj_upload_file = upload_file("file")
            # generate embeddings
            obj_faiss_vector_db = vector_db("faiss") 
            
            # loop all PDF files
            for pdf in pdfs:
                # vector store name
                store_name = f"{pdf.name[:-4]}.faiss"
                # check store exits
                if not obj_faiss_vector_db.store_exists(store_name):
                    # uploaded files
                    if obj_upload_file.upload_file(self.__directory, pdf):
                        # get chunks from uploaded file
                        chunks = self.read_and_textify_pdf(pdf)
                        obj_faiss_vector_db.save_vector_db(store_name, chunks)
                    else:
                        st.write("File upload failed.")  
                else:
                    st.write("PDF: FAISS index is exists.")    
                        
    def read_and_textify_pdf(self, pdf):
        # concate pdf path
        pdf_path = os.path.join(self.__directory, pdf.name)
        # read file file and get file text
        file_reader = PDFMinerLoader(pdf_path)
        file_text = file_reader.load()
        
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = int(os.environ['chunk_size']),
            chunk_overlap = int(os.environ['chunk_overlap']),
            length_function = len
        )
        
        chunks = text_splitter.split_text(text = file_text[0].page_content)
        return chunks
