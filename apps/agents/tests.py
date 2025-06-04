# # from django.test import TestCase
# # Create your tests here.

# import os, getpass

# def _set_env(var: str):
#     if not os.environ.get(var):
#         os.environ[var] = getpass.getpass(f"{var}: ")

# _set_env("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")
# _set_env("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")
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_PROJECT"] = "simple_chatbot"

# from langgraph.graph import MessagesState
# from langchain_core.messages import HumanMessage, SystemMessage

# # System message
# sys_msg = SystemMessage(content="You are a helpful assistant.")

# # Node
# def assistant(state: MessagesState):
#    return {"messages": [llm.invoke([sys_msg] + state["messages"])]}


# from langgraph.graph import START, StateGraph
# from IPython.display import Image, display

# # Graph
# builder = StateGraph(MessagesState)

# builder.add_node("assistant", assistant)
# builder.add_edge(START, "assistant")
# react_graph = builder.compile()

# # Show
# display(Image(react_graph.get_graph(xray=True).draw_mermaid_png()))



# messages = [HumanMessage(content="Hi simple chat bot")]
# messages = react_graph.invoke({"messages": messages})
# for m in messages['messages']:
#     m.pretty_print()



# from langgraph.checkpoint.memory import MemorySaver
# memory = MemorySaver()
# react_graph = builder.compile(checkpointer=memory)


# messages = [HumanMessage(content="What is my name")]
# messages = react_graph.invoke({"messages": messages},config={"thread_id": "unique_thread_id_123"})
# for m in messages['messages']:
#     m.pretty_print()


