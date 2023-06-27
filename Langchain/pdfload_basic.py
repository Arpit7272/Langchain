from langchain.llms import OpenAI
import os
from config import key
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings,HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA


#----------------File Export----------------------------
import pytesseract
from pdf2image import convert_from_path

template  = """
I am going to provide  data and from that data, i need the below fields and output in  below provided format in which each block will have below values:
1. Provider Name: Organisation or Institute who has authorized the certificate
2. Credit Type
3. Total Credit in digits
4. Issued date: It is the date present in the row field, if not get the certificate date
5. Title: Its Activity Name or Topic Name present for each row.
Format: Json (described below)
[ "provider name"  :  "Output" ,
"Credit Type" : "Output",
"Total Credit " : " Output",
"Issued date" : " Output",
"Title" : "Output"
]
[above fields again for other values]
Here output is the value from your response
"""

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

#-----------------------Document Analysis -----------------------------
os.environ["OPENAI_API_KEY"] = key
llm = OpenAI(temperature = 0.9,model_name = 'text-davinci-003', verbose= True)
certificate_text = image_text_extraction("/Users/arpit/Python/OpenAI/utilities/Langchain/transcript/_AAFP Transcript 3282022.pdf")
documents = [Document(page_content=certificate_text)]
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
# embeddings = HuggingFaceEmbeddings()
embeddings = OpenAIEmbeddings(model = 'text-davinci-003')
db = Chroma.from_documents(texts, embeddings)
retriever = db.as_retriever(search_kwargs={"k": 1})

qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)
print(qa.run(template))
condition = input("Type your question. Type 'exit' to stop.\n")
print("-------Output------\n")
while condition!='exit':
  print(qa.run(template))
  condition = input("\nType your question. Type 'exit' to stop.\n")