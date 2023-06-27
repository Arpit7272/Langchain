import os
from config import key, serp_api
from langchain.utilities import GoogleSerperAPIWrapper
from langchain.agents import load_tools,initialize_agent
from langchain.llms.openai import OpenAI

os.environ["OPENAI_API_KEY"] = key
os.environ["SERPAPI_API_KEY"] = serp_api

#--------API through Langchain
llm = OpenAI(temperature=0)

tool_names = ['serpapi']
tools = load_tools(tool_names)
agent = initialize_agent(tools, llm, agent='zero-shot-react-description', verbose=False)  #verbose=true will display how the system is working

print(agent.run('What is Langchain?'))

#  To check API
search = GoogleSerperAPIWrapper()
print(search.run("Obama's first name?"))
#