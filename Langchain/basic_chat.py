from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain import PromptTemplate, LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    HumanMessagePromptTemplate
)
from langchain.schema import (
  AIMessage,
  HumanMessage,
  SystemMessage
)
import os
from config import key

os.environ["OPENAI_API_KEY"] = key
chat = ChatOpenAI(temperature=0)
print(chat([HumanMessage(content="Translate this sentence from English to French. I love programming.")]))