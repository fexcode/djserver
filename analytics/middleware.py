# analytics/middleware.py
import time
from asgiref.sync import sync_to_async, async_to_sync
from django.utils import timezone
from .models import AccessLog

class AccessLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.time()
        response = self.get_response(request)
        duration = time.time() - start

        # 把异步函数包成同步调用，自动丢线程池
        async_to_sync(self.log_async)(request, response, duration)
        return response

    @sync_to_async
    def log_async(self, request, response, duration):
        AccessLog.objects.create(
            user=request.user if request.user.is_authenticated else None,
            ip=self.get_client_ip(request),
            user_agent=request.META.get("HTTP_USER_AGENT", "")[:1000],
            method=request.method,
            path=request.get_full_path(),
            status_code=response.status_code,
            duration=timezone.timedelta(seconds=duration),
        )

    @staticmethod
    def get_client_ip(request):
        x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
        return x_forwarded.split(",")[0].strip() if x_forwarded else request.META.get("REMOTE_ADDR")