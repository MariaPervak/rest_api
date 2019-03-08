from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from rest_api.models import FilesData
from rest_api.serializers import FilesDataSerializers, FilesDataPostSerializers

class Files(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        files = FilesData.objects.all()
        serializer = FilesDataSerializers(files, many=True)
        return Response(serializer.data)

    def post(self, request):

        files = FilesDataPostSerializers(data=request.data)
        if files.is_valid():
            files.save()
            return Response('File added successfully')
        else:
            return Response('Error')



# Create your views here.
