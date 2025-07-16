#!/usr/bin/env python3
"""
Serializers for User, Conversation, and Message models.

These serializers handle:
- Flat serialization for User
- Nested serialization for Messages within Conversations
- Representation of sender info within messages

Nested relationships allow API consumers to view conversation threads with user and message data.
"""

from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.

    Includes essential user identity fields. Password is excluded for security.
    """
    class Meta:
        model = User
        fields = [
            'user_id',
            'username',
            'email',
            'first_name',
            'last_name',
            'phone_number',
        ]


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for Message instances.

    Embeds sender details using the UserSerializer.
    Sender is read-only to ensure it’s derived from the authenticated user.
    """
    sender = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = [
            'message_id',
            'conversation',
            'sender',
            'message_body',
            'sent_at',
        ]
        read_only_fields = ['sent_at']


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for Conversation instances.

    Includes:
    - Participants serialized as user details.
    - Messages nested via MessageSerializer.
    """
    participants = UserSerializer(many=True, read_only=True)
    messages = MessageSerializer(many=True, read_only=True, source='messages')

    class Meta:
        model = Conversation
        fields = [
            'conversation_id',
            'participants',
            'created_at',
            'messages',
        ]
        read_only_fields = ['created_at']
