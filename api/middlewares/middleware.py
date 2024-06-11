import time
from django.http import JsonResponse
import re
import math


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)
        end_time = time.time()
        duration = end_time - start_time

        with open("api/middlewares/requests.log", "a") as file:
            file.write(
                f"{request.user} {request.method} {request.path} {duration} {response.status_code}\n"
            )

        return response


class OnlyAdminMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        If user is not a superuser or staff and tries to access endpoints under /api/v1/admin/*,
        return 403 Forbidden.
        """
        if re.match(r"^/api/v1/admin/", request.path):
            if not request.user.is_authenticated or not (
                request.user.is_superuser or request.user.is_staff
            ):
                return JsonResponse(
                    {"message": "You are not authorized to access this endpoint"},
                    status=403,
                )

        return self.get_response(request)
