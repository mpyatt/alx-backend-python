from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout, get_user_model
from .models import Message

User = get_user_model()


@require_http_methods(["DELETE"])
@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return JsonResponse({'detail': 'User account deleted successfully.'}, status=204)


@login_required
def threaded_conversation(request):
    messages = Message.objects.filter(
        sender=request.user,
        parent_message__isnull=True
    ).select_related('sender', 'receiver').prefetch_related('replies')

    response = []
    for message in messages:
        thread = {
            'id': message.id,
            'content': message.content,
            'replies': [
                {'id': reply.id, 'content': reply.content}
                for reply in message.replies.all()
            ]
        }
        response.append(thread)

    return JsonResponse({'threads': response})


@login_required
def unread_messages(request):
    messages = Message.unread.for_user(request.user)
    data = [
        {
            'id': msg.id,
            'sender_id': msg.sender_id,
            'content': msg.content,
            'timestamp': msg.timestamp,
        }
        for msg in messages
    ]
    return JsonResponse({'unread_messages': data})
