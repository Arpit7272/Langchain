from langchain.llms import OpenAI
import os
from config import key
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings,HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA


#----------------Text Extraction----------------------------
import pytesseract
from pdf2image import convert_from_path

def image_text_extraction(filepath):
    output = ""
    # Convert the PDF file to a list of PIL images
    images = convert_from_path(filepath)
    # Loop through each page and extract text using Tesseract OCR
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        output += f"Page {i+1}:\n{text}\n" 

    return output    
#---------------------------------------------------------------------


#-----------Loaderclass Creation----------------------
from typing import List, Optional

from langchain.docstore.document import Document
from langchain.document_loaders.base import BaseLoader


class ImageLoader(BaseLoader):
    """Load text files."""
    def __init__(self, file_path: str, encoding: Optional[str] = None):
        """Initialize with file path."""
        self.file_path = file_path
        self.encoding = encoding

    def load(self) -> List[Document]:
        """Load from file path."""
        with open(self.file_path, encoding=self.encoding) as f:
            text = image_text_extraction(self.file_path)
        metadata = {"source": self.file_path}
        return [Document(page_content=text, metadata=metadata)]


#-----------------------Document Analysis one after other in directory -----------------------------
os.environ["OPENAI_API_KEY"] = key
llm = OpenAI(temperature = 0,model_name = 'text-davinci-003')
directory =  "/Users/arpit/Python/OpenAI/utilities/Langchain/transcript"
file_list = os.listdir(directory)
for file_name in file_list:
    file_path = os.path.join(directory, file_name)
    if not file_path.lower().endswith('.pdf'):
        continue
    loader = ImageLoader(file_path)
    docs = loader.load()
    # text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    # texts = text_splitter.split_documents(docs)
    embeddings = OpenAIEmbeddings()
    db = Chroma.from_documents(docs, embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 1})

    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
    print("\nFILE LOADED: ", file_name)
    query = input("Type your question. Type 'exit' to stop.Type 'skip' to next document.\n")
    print("\n-------Output------\n")
    while query!='skip' and query.lower() != 'exit':
        print(qa.run(query))
        query = input("\nType your question. Type 'skip' to next document. Type 'exit' to stop.\n")
    if query.lower() == 'exit':
        break    
             