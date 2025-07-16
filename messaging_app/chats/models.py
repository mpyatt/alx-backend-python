#!/usr/bin/env python3
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custom user model extending Django's AbstractUser."""
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


class Conversation(models.Model):
    """Conversation model for tracking participants."""
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Conversation {self.id} - Participants: {[user.username for user in self.participants.all()]}"


class Message(models.Model):
    """Message model representing a single message in a conversation."""
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sent_messages')
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name='messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:30]}..."
