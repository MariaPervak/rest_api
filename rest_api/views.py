from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from django.shortcuts import get_object_or_404
from django.conf import settings

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


    def get(self, request, pk=''):

        if pk:
            try:
                file_to_upload = FilesData.objects.get(id=pk).image_name
            except Exception:
                return Response("The file doesn't exist")

            try:
                path_to_upload = request.data['path']
            except Exception:
                return Response("Enter the full path to your folder")

            try:
                with open(path_to_upload + file_to_upload, "wb") as file_handler:
                    ufr = requests.get( settings.SITE_URL + '/media/upload/' + file_to_upload)
                    file_handler.write(ufr.content)
                    file_handler.close()
                    return Response('The file has been succesfully downloaded')
            except Exception:
                    return Response("Something goes wrong. Check the full path to your folder")

        else:
            files = FilesData.objects.all()
            serializer = FilesDataSerializers(files, many=True)
            return Response(serializer.data)


    def post(self, request):

        try:
            path_to_upload = request.data['path']
        except Exception:
            return Response('Enter the full path to your folder')

        path_uploaded = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/media/upload/'
        files_list = FilesData.objects.values_list('image_name', flat=True)
        files_to_upload = [f for f in listdir(path_to_upload) if isfile(join(path_to_upload, f))]
        new_files = [file for file in files_to_upload if not file in list(files_list)]

        if not new_files:
             return Response('There is nothing to add')

        queue = Queue()
        for i in range(len(new_files)):
            name = "Thread %s" % (i+1)
            t = Uploader(queue, name, path_to_upload, path_uploaded)
            t.setDaemon(True)
            t.start()

        for file in new_files:
            queue.put(file)
        queue.join()

        return Response('The file(s) have been added successfully')


    def delete(self, request, pk):
        path_uploaded = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/media/upload/'
        try:
            file_to_delete = FilesData.objects.get(id=pk).image_name
        except Exception:
            return Response("The file doesn't exist")
        os.remove(path_uploaded + file_to_delete)
        file = get_object_or_404(FilesData.objects.all(), pk=pk)
        file.delete()
        return Response('The file has been deleted successfully')
