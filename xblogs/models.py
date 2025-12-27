from django.db import models



class ReadRecord(models.Model):
    id = models.AutoField(primary_key=True)
    uid = models.IntegerField(verbose_name="用户id")
    blog_id = models.IntegerField(verbose_name="博客id", db_index=True)  # 索引
    read_time = models.DateTimeField(verbose_name="访问时间", auto_now_add=True)
    unlogined = models.BooleanField(verbose_name="是否未登录", default=False)

    class Meta:
        verbose_name = "阅读记录"
        verbose_name_plural = verbose_name
