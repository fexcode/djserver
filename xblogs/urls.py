from django.urls import path
from .views import get_read_count, add_count, getall_read_count_sum

urlpatterns = [
    path("getall_read_count_sum", getall_read_count_sum, name="getall_read_count_sum"),
    path("get_read_count", get_read_count, name="get_read_count"),
    path("add_count", add_count, name="add_count"),
]
