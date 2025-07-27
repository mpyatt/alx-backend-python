from collections import defaultdict
from datetime import timedelta
from django.http import JsonResponse
from django.utils import timezone
import logging


# --- Logger Setup ---
logger = logging.getLogger("request_logger")
handler = logging.FileHandler("requests.log")
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


class RequestLoggingMiddleware:
    """
    Logs each user's requests with timestamp, user, and path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logger.info(f"{timezone.now()} - User: {user} - Path: {request.path}")
        return self.get_response(request)


class RestrictAccessByTimeMiddleware:
    """
    Restricts access to chat routes outside 6PM to 9PM.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_hour = timezone.now().hour
        if not (18 <= current_hour <= 21):
            return JsonResponse(
                {"detail": "Chat access is restricted to 6PM - 9PM only."},
                status=403
            )
        return self.get_response(request)


class OffensiveLanguageMiddleware:
    """
    Limits users to 5 POSTs/minute to /api/messages to prevent abuse.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.message_logs = defaultdict(list)

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith("/api/messages"):
            ip = self.get_client_ip(request)
            now = timezone.now()

            recent_timestamps = [
                ts for ts in self.message_logs[ip]
                if now - ts < timedelta(minutes=1)
            ]
            self.message_logs[ip] = recent_timestamps

            if len(recent_timestamps) >= 5:
                return JsonResponse(
                    {"detail": "Rate limit exceeded: Max 5 messages per minute."},
                    status=429
                )

            self.message_logs[ip].append(now)

        return self.get_response(request)

    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            return x_forwarded_for.split(",")[0].strip()
        return request.META.get("REMOTE_ADDR")


class RolepermissionMiddleware:
    """
    Restricts access to chat features to users with 'admin' or 'moderator' roles.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        protected_paths = ["/api/moderate",
                           "/api/admin/ban", "/api/messages/delete"]

        if request.path in protected_paths:
            if not request.user.is_authenticated:
                return JsonResponse({"detail": "Authentication required."}, status=401)

            user_role = getattr(request.user, "role", None)

            if user_role not in ["admin", "moderator"]:
                return JsonResponse(
                    {"detail": "Permission denied: admin or moderator role required."},
                    status=403
                )

        return self.get_response(request)
