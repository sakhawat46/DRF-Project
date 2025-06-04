# chat_app/urls.py
from django.urls import path
from .views import (
    ConversationListCreateView,
    ConversationDetailView,
    MessageCreateView
)

urlpatterns = [
    path('conversations/', ConversationListCreateView.as_view(), name='conversation-list'),
    path('conversations/<int:pk>/', ConversationDetailView.as_view(), name='conversation-detail'),
    path('conversations/<int:conversation_id>/messages/', MessageCreateView.as_view(), name='message-create'),
]