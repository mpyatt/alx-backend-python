from django.http import JsonResponse
from datetime import datetime
import logging

# Configure logger
logger = logging.getLogger("request_logger")
handler = logging.FileHandler("requests.log")
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.setLevel(logging.INFO)
logger.addHandler(handler)


class RequestLoggingMiddleware:
    """
    Middleware to log each user’s requests including timestamp, user and path.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else "Anonymous"
        logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")
        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    """
    Middleware that restricts access to the chat app outside 6PM to 9PM.
    Returns 403 Forbidden if accessed outside allowed hours.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get current hour (24-hour format)
        current_hour = datetime.now().hour

        # Allow access only between 18 (6PM) and 21 (9PM) inclusive
        if not (18 <= current_hour <= 21):
            return JsonResponse(
                {"detail": "Chat access is restricted to 6PM - 9PM only."},
                status=403
            )

        return self.get_response(request)
