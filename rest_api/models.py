from django.db import models


class FilesData(models.Model):
    image_name = models.CharField(max_length=200)
