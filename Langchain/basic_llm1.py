from langchain.llms import OpenAI
import os
from config import key

os.environ["OPENAI_API_KEY"] = key
llm = OpenAI(temperature = 0,verbose=True)

print(llm("Who is CEO of Georgia Power Company, and what is your knowledge cutoff date?"))
llm.save("llm.json")

# llm_result = llm.generate(["Tell me a joke in 1 line","Tell me a poem in 1 line"] * 15)

# # print(llm_result.generations)
# # print(llm_result.generations[-1])

# print(llm_result.llm_output)
