import os
import config
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.document_loaders.image import UnstructuredImageLoader

os.environ["OPENAI_API_KEY"] = key
os.environ["SERPER_API_KEY"] = serp_api



llm = OpenAI(temperature=0.9)
prompt = PromptTemplate(
  input_variables=["topic"],
  template="What is {topic} explain in one line.",
)

#----------BASIC LLM EXAMPLE----------------
# text = "What is Ruby on Rails explain in 1 line"
# print(llm(text))

#-------------TEMPLATE FORMAT------------
# print(prompt.format(topic="Ruby on Rails"))

#--------------CHAIN TO Use this prompt for llm analysis-------
chain = LLMChain(llm=llm, prompt=prompt)
# print(chain.run("Ruby on Rails"))

#-------------Loaders-------------------------
# training_NETCE.pdf

loader = UnstructuredImageLoader("../../../Downloads/certificate.pdf")
data = loader.load()

print(data[0])
