from rest_framework.permissions import BasePermission


class IsOwnerOrParticipant(BasePermission):
    """
    Allows access only to the owner or a participant of a conversation/message.
    """

    def has_object_permission(self, request, view, obj):
        return request.user == obj.user or request.user in obj.participants.all()
