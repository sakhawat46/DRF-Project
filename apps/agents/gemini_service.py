# services/gemini_service.py
import google.generativeai as genai

class GeminiService:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def generate_response(self, prompt, conversation_history=None):
        if conversation_history is None:
            conversation_history = []
        
        # Format the conversation history for Gemini
        chat = self.model.start_chat(history=conversation_history)
        response = chat.send_message(prompt)
        return response.text