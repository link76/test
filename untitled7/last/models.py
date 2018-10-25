from django.db import models


class Notice(models.Model):
    notice_title = models.CharField(max_length=32)
    notice_data = models.TextField()
    notice_picture = models.CharField(max_length=32)
    notice_time = models.CharField(max_length=20)

    def __str__(self):
        return self.notice_title
