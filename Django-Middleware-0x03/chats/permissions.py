from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to only allow participants of a conversation to access it.
    """

    def has_permission(self, request, view):
        # Only allow authenticated users
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Get the conversation from the object (works for both Conversation and Message)
        conversation = getattr(obj, 'conversation', obj)

        # For unsafe methods, explicitly check participant access
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user in conversation.participants.all()

        # For safe methods (GET, HEAD, OPTIONS), allow if participant
        return request.user in conversation.participants.all()
