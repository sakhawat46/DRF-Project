# # views.py
# from rest_framework import generics, status
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from .models import Conversation, Message
# from .serializers import ConversationSerializer, MessageSerializer
# from .conversation_agent import ConversationAgent
# from django.conf import settings

# class ConversationListCreateView(generics.ListCreateAPIView):
#     serializer_class = ConversationSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         return Conversation.objects.filter(user=self.request.user)
    
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

# class ConversationDetailView(generics.RetrieveDestroyAPIView):
#     serializer_class = ConversationSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         return Conversation.objects.filter(user=self.request.user)

# class MessageCreateView(generics.CreateAPIView):
#     serializer_class = MessageSerializer
#     permission_classes = [IsAuthenticated]
    
#     def create(self, request, *args, **kwargs):
#         conversation_id = kwargs.get('conversation_id')
#         try:
#             conversation = Conversation.objects.get(id=conversation_id, user=request.user)
#         except Conversation.DoesNotExist:
#             return Response(
#                 {"error": "Conversation not found"}, 
#                 status=status.HTTP_404_NOT_FOUND
#             )
        
#         # Save user message
#         user_message = Message.objects.create(
#             conversation=conversation,
#             content=request.data['content'],
#             role='user'
#         )
        
#         # Initialize agent and get response
#         agent = ConversationAgent(settings.GEMINI_API_KEY)
#         result = agent.run(conversation_id, request.data['content'])
        
#         # Save assistant response
#         assistant_message = Message.objects.create(
#             conversation=conversation,
#             content=result['response'],
#             role='assistant'
#         )
        
#         # Update conversation timestamp
#         conversation.save()
        
#         # Return both messages
#         serializer = self.get_serializer([user_message, assistant_message], many=True)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)


# chat_app/views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound
from django.conf import settings
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer
from .conversation_agent import ConversationAgent

class ConversationListCreateView(generics.ListCreateAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Return only conversations belonging to the current user"""
        return Conversation.objects.filter(user=self.request.user).order_by('-updated_at')

    def perform_create(self, serializer):
        """Automatically assign the current user to new conversations"""
        serializer.save(user=self.request.user)

class ConversationDetailView(generics.RetrieveDestroyAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Ensure users can only access their own conversations"""
        return Conversation.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        """Custom delete handling if needed"""
        super().perform_destroy(instance)

class MessageCreateView(generics.CreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    queryset = Message.objects.none()  # Required for DRF but we don't need listing

    def create(self, request, *args, **kwargs):
        """Handle message creation and AI response generation"""
        conversation_id = self.kwargs['conversation_id']
        
        try:
            # Verify conversation exists and belongs to user
            conversation = Conversation.objects.get(
                id=conversation_id,
                user=self.request.user
            )
        except Conversation.DoesNotExist:
            raise NotFound("Conversation not found or access denied")

        # Validate user message
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Save user message
        user_message = Message.objects.create(
            conversation=conversation,
            content=serializer.validated_data['content'],
            role='user'
        )

        try:
            # Get AI response
            agent = ConversationAgent(settings.GEMINI_API_KEY)
            ai_response = agent.run(
                conversation_id,
                serializer.validated_data['content']
            )['response']

            # Save AI response
            assistant_message = Message.objects.create(
                conversation=conversation,
                content=ai_response,
                role='assistant'
            )

            # Update conversation timestamp
            conversation.save()

            # Return both messages
            output_serializer = MessageSerializer(
                [user_message, assistant_message],
                many=True
            )
            return Response(output_serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Log the error for debugging
            import logging
            logging.error(f"AI processing error: {str(e)}")
            return Response(
                {"error": "Failed to generate AI response"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )