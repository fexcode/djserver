from django.contrib import admin
from .models import AccessLog

@admin.register(AccessLog)
class AccessLogAdmin(admin.ModelAdmin):
    list_display = ["timestamp", "ip", "method", "path", "status_code", "user", "duration"]
    list_filter = ["status_code", "method", "timestamp"]
    search_fields = ["ip", "path", "user_agent"]
    date_hierarchy = "timestamp"
    show_full_result_count = False   # 数据量大时加速