from rest_framework.permissions import BasePermission


class IsParticipantOfConversation(BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it or its messages.
    """

    def has_object_permission(self, request, view, obj):
        """
        Check if the user is part of the conversation.
        Applies to both Conversation and Message objects.
        """
        # For a Message object, get the conversation
        conversation = getattr(obj, 'conversation', obj)
        return request.user in conversation.participants.all()
