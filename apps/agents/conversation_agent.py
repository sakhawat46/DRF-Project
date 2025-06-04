# # agents/conversation_agent.py
# from typing import TypedDict, List
# from langgraph.graph import StateGraph, END
# from services.gemini_service import GeminiService

# class AgentState(TypedDict):
#     conversation_id: str
#     user_input: str
#     messages: List[dict]
#     response: str

# class ConversationAgent:
#     def __init__(self, gemini_api_key):
#         self.gemini = GeminiService(gemini_api_key)
#         self.workflow = self._create_workflow()
    
#     def _create_workflow(self):
#         workflow = StateGraph(AgentState)
        
#         # Define nodes
#         workflow.add_node("retrieve_history", self.retrieve_history)
#         workflow.add_node("generate_response", self.generate_response)
#         workflow.add_node("update_conversation", self.update_conversation)
        
#         # Define edges
#         workflow.set_entry_point("retrieve_history")
#         workflow.add_edge("retrieve_history", "generate_response")
#         workflow.add_edge("generate_response", "update_conversation")
#         workflow.add_edge("update_conversation", END)
        
#         return workflow.compile()
    
#     def retrieve_history(self, state: AgentState):
#         # This will be implemented with your Django models
#         return {"messages": []}  # Placeholder
    
#     def generate_response(self, state: AgentState):
#         response = self.gemini.generate_response(
#             state["user_input"],
#             state["messages"]
#         )
#         return {"response": response}
    
#     def update_conversation(self, state: AgentState):
#         # This will save the new messages to your Django models
#         return state
    
#     def run(self, conversation_id, user_input):
#         return self.workflow.invoke({
#             "conversation_id": conversation_id,
#             "user_input": user_input,
#             "messages": [],
#             "response": ""
#         })




# chat_app/agents/conversation_agent.py
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from .gemini_service import GeminiService

class AgentState(TypedDict):
    conversation_id: str
    user_input: str
    messages: List[dict]
    response: str

class ConversationAgent:
    def __init__(self, gemini_api_key):
        self.gemini = GeminiService(gemini_api_key)
        self.workflow = self._create_workflow()
    
    def _create_workflow(self):
        workflow = StateGraph(AgentState)
        
        workflow.add_node("retrieve_history", self.retrieve_history)
        workflow.add_node("generate_response", self.generate_response)
        workflow.add_node("update_conversation", self.update_conversation)
        
        workflow.set_entry_point("retrieve_history")
        workflow.add_edge("retrieve_history", "generate_response")
        workflow.add_edge("generate_response", "update_conversation")
        workflow.add_edge("update_conversation", END)
        
        return workflow.compile()
    
    def retrieve_history(self, state: AgentState):
        """Retrieve conversation history from database"""
        from .models import Message  # Local import to avoid circular imports
        
        messages = Message.objects.filter(
            conversation_id=state["conversation_id"]
        ).order_by('timestamp')
        
        formatted_history = []
        for msg in messages:
            formatted_history.append({
                "role": msg.role,
                "parts": [msg.content]
            })
        
        return {"messages": formatted_history}
    
    def generate_response(self, state: AgentState):
        response = self.gemini.generate_response(
            state["user_input"],
            state["messages"]
        )
        return {"response": response}
    
    def update_conversation(self, state: AgentState):
        # Implementation to save messages would go here
        return state
    
    def run(self, conversation_id, user_input):
        return self.workflow.invoke({
            "conversation_id": conversation_id,
            "user_input": user_input,
            "messages": [],
            "response": ""
        })