from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout, get_user_model

User = get_user_model()


@require_http_methods(["DELETE"])
@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return JsonResponse({'detail': 'User account deleted successfully.'}, status=204)
