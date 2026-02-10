from typing_extensions import TypedDict
from langgraph.graph import START, StateGraph, END
from langchain_ollama import ChatOllama
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain.messages import SystemMessage, HumanMessage
from langchain.tools import tool


from dotenv import load_dotenv

load_dotenv()

chat_model = ChatOllama(model= "qwen3:8b")
translate_model = ChatOllama(model= "translategemma:4b")

# result = chat_model.invoke("hi")
messages = (SystemMessage(content=""" You are a professional English (en) to Hindi (hi) translator. Your goal is to accurately convey the meaning and nuances of the original english text while adhering to hi grammar, vocabulary, and cultural sensitivities.
Produce only the hi translation, without any additional explanations or commentary."""), HumanMessage("""Please translate the following english text into hindi : John Galt was among the most popular and prolific Scottish writers
of the nineteenth century. He wrote in a panoply of forms and genres
about a great variety of topics and settings, drawing on his experiences
of living, working, and travelling in Scotland and England, in Europe
and the Mediterranean, and in North America"""))
result = translate_model.invoke(messages)

print(result.content)