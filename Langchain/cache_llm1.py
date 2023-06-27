from langchain.llms import OpenAI
from langchain.cache import InMemoryCache
import os
import time
import langchain
from config import key

os.environ["OPENAI_API_KEY"] = key
#-----------Cache----------------
langchain.llm_cache = InMemoryCache()

llm = OpenAI(model_name = 'text-ada-001', temperature = 0)

start_time  =  time.time()
print(llm("Tell me a joke in 1 line"))
end_time = time.time()
print(end_time - start_time)

#---------Time after caching
start_time  =  time.time()
print(llm("Tell me a joke in 1 line"))
end_time = time.time()
print(end_time - start_time)


