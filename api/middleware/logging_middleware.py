import time


class LoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start_time = time.time()

        response = self.get_response(request)
        print(request.method, request.path, time.time() - start_time, request.user)
        end_time = time.time()
        duration = end_time - start_time

        with open("api/middleware/log.txt", "a") as file:
            file.write(f"{request.method} {request.path} {duration}\n")

        return response
