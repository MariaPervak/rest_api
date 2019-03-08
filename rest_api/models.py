from django.db import models
# from django.contrib.auth.models import User
# from djoser.urls.base import User


class FilesData(models.Model):
    image_path = models.CharField(max_length=200)
