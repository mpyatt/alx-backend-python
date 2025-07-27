#!/usr/bin/env python3
"""
ViewSets for managing conversations and messages.

Includes logic to list, create, and retrieve message and conversation data
using Django REST Framework's ModelViewSet.
"""

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from .models import Conversation, Message, User
from .serializers import (
    ConversationSerializer,
    MessageSerializer
)


class ConversationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and creating Conversations.

    - GET /api/conversations/ → list all conversations for the current user
    - POST /api/conversations/ → create a new conversation
    """
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Only return conversations where the current user is a participant.
        """
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        """
        Create a new conversation with a list of participant user_ids.
        """
        user_ids = request.data.get("user_ids", [])
        if not user_ids or len(user_ids) < 2:
            return Response(
                {"detail": "At least two participants are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        participants = User.objects.filter(user_id__in=user_ids)
        if participants.count() < 2:
            return Response(
                {"detail": "Some user_ids are invalid."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversation = Conversation.objects.create()
        conversation.participants.set(participants)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing and sending messages.

    - GET /api/messages/ → list all messages in conversations the user participates in
    - POST /api/messages/ → send a new message
    """
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['conversation']

    def get_queryset(self):
        """
        Only return messages from conversations where the current user is a participant.
        """
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        """
        Automatically set the sender as the current user when creating a message.
        Ensure the sender is a participant in the conversation.
        """
        conversation_id = self.request.data.get("conversation")

        if not conversation_id:
            return Response(
                {"detail": "Missing conversation_id."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            conversation = Conversation.objects.get(id=conversation_id)
        except Conversation.DoesNotExist:
            return Response(
                {"detail": "Conversation not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if self.request.user not in conversation.participants.all():
            return Response(
                {"detail": "You are not a participant in this conversation."},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer.save(sender=self.request.user, conversation=conversation)
