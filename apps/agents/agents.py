from typing import TypedDict, Annotated, Sequence
import operator
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI

import google.generativeai as genai

from langchain_openai import ChatOpenAI
from django.conf import settings

# llm = ChatOpenAI(
#     model="gpt-3.5-turbo",
#     openai_api_key=settings.OPENAI_API_KEY
# )



genai.configure(api_key=settings.GEMINI_API_KEY)
llm = genai.GenerativeModel('gemini-2.0-flash')



# Define the state
class AgentState(TypedDict):
    messages: Annotated[Sequence[HumanMessage | AIMessage], operator.add]

# Set up the LLM
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Define the nodes
def chatbot_node(state: AgentState):
    last_message = state['messages'][-1]
    response = llm.invoke(state['messages'])
    return {"messages": [response]}

# Build the graph
workflow = StateGraph(AgentState)
workflow.add_node("chatbot", chatbot_node)
workflow.add_edge("chatbot", END)
workflow.set_entry_point("chatbot")

# Compile the graph
agent = workflow.compile()