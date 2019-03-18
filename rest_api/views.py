from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from django.shortcuts import get_object_or_404

import os
from os import listdir
from os.path import isfile, join

from threading import Thread
from queue import Queue

import requests

from rest_api.models import FilesData
from rest_api.serializers import FilesDataSerializers
from .threads import *



class Files(APIView):

    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]


    def get(self, request):
        f=open(r'/home/maria/temp/temp/y_39e94878.jpg',"wb")
        ufr = requests.get("https://pp.userapi.com/c5571/u28104454/-6/y_39e94878.jpg")
        f.write(ufr.content)
        f.close()


        files = FilesData.objects.all()
        serializer = FilesDataSerializers(files, many=True)
        return Response(serializer.data)


    def post(self, request):
        request_dict = request.data.dict()
        print(request_dict['path'])
        # path_to_upload = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/static/to_upload/'
        path_to_upload = request_dict['path']
        path_uploaded = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/static/upload/'

        files_list = FilesData.objects.values_list('image_path', flat=True)
        files_to_upload = [f for f in listdir(path_to_upload) if isfile(join(path_to_upload, f))]
        new_files = [file for file in files_to_upload if not file in list(files_list)]

        if not new_files:
            return Response('There is nothing to add')
        else:
            queue = Queue()
            for i in range(len(new_files)):
                name = "Поток %s" % (i+1)
                t = Uploader(queue, name, path_to_upload, path_uploaded)
                t.setDaemon(True)
                t.start()

            for file in new_files:
                queue.put(file)
            queue.join()

            return Response('The file(s) have been added successfully')


    def delete(self, request, pk):
        path_uploaded = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/static/upload/'

        file_to_delete = FilesData.objects.get(id=pk).image_path
        os.remove(path_uploaded + file_to_delete)
        file = get_object_or_404(FilesData.objects.all(), pk=pk)
        file.delete()
        return Response('The file has been deleted successfully')

class DownloadFile(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, pk):
        return Response('Hey dude')
