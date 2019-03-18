from rest_framework import serializers
from rest_api.models import FilesData

class FilesDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = FilesData
        fields = ("id", "image_path")

class FilesDataPostSerializers(serializers.ModelSerializer):
    class Meta:
        model = FilesData
        fields = ["id", "image_path"]
