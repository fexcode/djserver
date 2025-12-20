from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """扩展用户表：加贡献点"""
    contrib_points = models.IntegerField("贡献点", default=0, blank=True)

    def __str__(self):
        return f"{self.username}({self.contrib_points})"