#!/usr/bin/env python3
"""
Serializers for User, Conversation, and Message models.

Includes validation and nested serialization for Conversations and Messages.
"""

from rest_framework import serializers
from .models import User, Conversation, Message


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the custom User model.
    Uses CharField explicitly for phone_number.
    """
    phone_number = serializers.CharField()

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
    Serializer for a single Message.
    Displays sender's full name using SerializerMethodField.
    """
    sender_name = serializers.SerializerMethodField()

    def get_sender_name(self, obj):
        """Returns sender's full name."""
        return f"{obj.sender.first_name} {obj.sender.last_name}".strip()

    class Meta:
        model = Message
        fields = [
            'message_id',
            'conversation',
            'sender',
            'sender_name',
            'message_body',
            'sent_at',
        ]
        read_only_fields = ['sent_at', 'sender', 'sender_name']

    def validate_message_body(self, value):
        """Ensure message is not empty."""
        if not value.strip():
            raise serializers.ValidationError("Message body cannot be empty.")
        return value


class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer for a Conversation.
    Includes participants and nested messages.
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
