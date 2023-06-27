from langchain.llms import OpenAI
import os
from config import key
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.chains import RetrievalQA

os.environ["OPENAI_API_KEY"] = key
llm = OpenAI(temperature = 0,model_name = 'text-davinci-003',verbose=True)

loader = TextLoader('test_doc.txt', encoding='utf8')
documents = loader.load()
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
texts = text_splitter.split_documents(documents)
embeddings = OpenAIEmbeddings()
db = Chroma.from_documents(texts, embeddings)
retriever = db.as_retriever()
qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=retriever)

query = input("Type your question. Type 'exit' to stop.\n")
print("-------Output------\n")
while query!='exit':
  print(qa.run(query))
  query = input("\nType your question. Type 'exit' to stop.\n")