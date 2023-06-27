from langchain.llms import OpenAI
import os
from langchain import PromptTemplate
from config import key
from langchain.chat_models import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings,HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA, LLMChain
import pandas as pd
import csv

#----------------Text Extraction----------------------------
import pytesseract
from pdf2image import convert_from_path

def image_text_extraction(filepath):
    output = ""
    # Convert the PDF file to a list of PIL images
    images = convert_from_path(filepath)
    # Loop through each page and extract text using Tesseract OCR
    for i, image in enumerate(images):
        data = pytesseract.image_to_string(image)
        output += f"Page {i+1}:\n{data}\n" 
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
            data = text
            lines = [line.strip() for line in data.split('\n') if line.strip()]
        metadata = {"source": self.file_path}
        # return [Document(page_content=text, metadata=metadata)]
        return text


#-----------------------Document Analysis one after other in directory -----------------------------
os.environ["OPENAI_API_KEY"] = key
llm = OpenAI(temperature = 0.6,model_name = 'text-davinci-003')
#----------PromptModel--------------------
# template  = """
# I am going to provide  data and from that data, i need the below fields and output in  below provided format in which each block will have below values:
# 1. Provider Name: Organisation or Institute who has authorized the certificate
# 2. Credit Type
# 3. Total Credit in digits
# 4. Issued date: It is the date present in the row field, if not get the certificate date
# 5. Title: Its Activity Name or Topic Name present for each row.
# Format: Json (described below)
# [ "provider name"  :  "Output" ,
# "Credit Type" : "Output",
# "Total Credit " : " Output",
# "Issued date" : " Output",
# "Title" : "Output"
# ]
# [above fields again for other values]
# Here output is the value from your response
# data : {text}
# """

template = """
Given the following data, extract the following fields and output them in the provided format:

Provider Name: The organization or institute that has authorized the certificate.
Credit Type: The type of credit obtained.
Total Credit (in digits).
Issued date: If available, use the date present in the row field; otherwise, use the certificate date.
Title: The activity or topic name for each row.
Data:
{text}
Output Format:
[  {    "provider name": "Output",    "Credit Type": "Output",    "Total Credit": "Output",    "Issued date": "Output",    "Title": "Output"  },  ...]
"""

# output_parser = StructuredOutputParser.from_response_schemas(repsonse_schemas)
# format_instruction = output_parser.get_format_instructions()
directory =  "/Users/arpit/Python/OpenAI/utilities/Langchain/transcript"
file_list = os.listdir(directory)
for file_name in file_list:
    file_path = os.path.join(directory, file_name)
    if not file_path.lower().endswith('.pdf'):
        continue
    loader = ImageLoader(file_path)
    docs = loader.load()

    print("\nFILE LOADED: ", file_name)
    print("\n-------Output------\n")
    query =''
    while query!='skip' and query.lower() != 'exit':
        prompt = PromptTemplate(
            input_variables=["text"],
            template= template,
            )
        chain = LLMChain(llm=llm, prompt=prompt)
        data = str(chain.run(text = docs))
        print(data)
        # # Testing---9
        # rows = data.split('\n')
        # header = rows[0].split(' | ')
        # data_rows = [row.split(' | ') for row in rows[1:]]
        # output_file = file_name +'.csv'
        # breakpoint()
        # print(f"Table saved as '{output_file}'.")

        query = input("\nType 'skip' to next document. Type 'exit' to stop.\n")
    if query.lower() == 'exit':
        break    
             