from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

def split_docs(docs, chunk_size = 1000, chunk_overlap= 200):
        print("Splitting docs...")
        # Initialize the text splitter with specified chunk size and overlap
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = chunk_size, chunk_overlap = chunk_overlap
        )
        # Split the documents into chunks
        splits = text_splitter.split_documents(docs)
        return splits
  


def load_docs_from_pdf_files(pdf_path):
        print("Loading docs from PDF file ...")
        # Initialize the PDF loader
        loader = PyPDFLoader(pdf_path)
        pages = []
        
        # Asynchronously load the pages from the PDF
        for page in loader.load():
            pages.append(page)
        return pages
   
