# analytics/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class AccessLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    ip = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=2048)
    status_code = models.PositiveSmallIntegerField()
    duration = models.DurationField()          # 耗时
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        verbose_name = "访问日志"
        verbose_name_plural = "访问日志"
        ordering = ["-timestamp"]

    def __str__(self):
        return f"[{self.timestamp:%Y-%m-%d %H:%M:%S}] {self.ip} {self.method} {self.path} → {self.status_code}"