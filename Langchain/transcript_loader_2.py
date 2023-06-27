from langchain.llms import OpenAI
import os
from langchain import PromptTemplate
from config import key, hugging_face
from langchain.memory import ConversationBufferMemory
from langchain.embeddings import OpenAIEmbeddings,HuggingFaceEmbeddings
from langchain.chains import LLMChain, ConversationChain
from getpass import getpass
from langchain import HuggingFaceHub

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
    return data    
#---------------------------------------------------------------------


HUGGINGFACEHUB_API_TOKEN = getpass()
os.environ["HUGGINGFACEHUB_API_TOKEN"] = hugging_face
#-----------------------Document Analysis one after other in directory -----------------------------
repo_id  = "openai-gpt"
llm = HuggingFaceHub(repo_id=repo_id, model_kwargs={"temperature":0.2, "max_length":490})

#----------PromptModel--------------------
template  ="""
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
data : {text}
"""


from langchain import PromptTemplate, LLMChain

prompt = PromptTemplate(template=template, input_variables=["text"])
llm_chain = LLMChain(prompt=prompt, llm=llm)

directory =  "/Users/arpit/Python/OpenAI/utilities/Langchain/transcript"
file_list = os.listdir(directory)
for file_name in file_list:
    file_path = os.path.join(directory, file_name)
    if not file_path.lower().endswith('.pdf'):
        continue
    data = image_text_extraction(file_path)
    print(llm_chain.run(data))
    print("\nFILE LOADED: ", file_name)
    print("\n-------Output------\n")
    query =''
    while query!='skip' and query.lower() != 'exit':
        data = image_text_extraction(file_path)
        print(llm_chain.run(data))
        query = input("\nType 'skip' to next document. Type 'exit' to stop.\n")
    if query.lower() == 'exit':
        break    
             