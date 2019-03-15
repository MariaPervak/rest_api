from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from django.shortcuts import get_object_or_404

import os
from os import listdir
from os.path import isfile, join

from rest_api.models import FilesData
from rest_api.serializers import FilesDataSerializers, FilesDataPostSerializers


class Files(APIView):

    permission_classes = [permissions.IsAuthenticated]
    # permission_classes = [permissions.AllowAny]


    def get(self, request):
        files = FilesData.objects.all()
        serializer = FilesDataSerializers(files, many=True)
        return Response(serializer.data)

    def post(self, request):
        path_to_upload = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/static/to_upload/'
        path_uploaded = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/static/upload/'

        files_list = FilesData.objects.values_list('image_path', flat=True)
        files_to_upload = [f for f in listdir(path_to_upload) if isfile(join(path_to_upload, f))]
        new_files = [file for file in files_to_upload if not file in list(files_list)]

        # for i, file in enumerate(new_files):
        #     interim_file = { 'file' + str(i) : open(path_to_upload + file) }

        if not new_files:
            return Response('There is nothing to add')
        else:
            for i, file in enumerate(new_files):
                with open(path_to_upload + file, 'rb') as f:
                    data = f.read()
                with open(path_uploaded + file, 'wb') as f:
                    f.write(data)

                dfile = FilesDataPostSerializers(data={'image_path' : file})
                if dfile.is_valid(raise_exception=True):
                    dfile.save()
                else:
                    return Response('Error')

            return Response('The file(s) have been added successfully')


    def delete(self, request, pk):
        path_uploaded = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/static/upload/'

        file_to_delete = FilesData.objects.get(id=pk).image_path
        os.remove(path_uploaded + file_to_delete)
        file = get_object_or_404(FilesData.objects.all(), pk=pk)
        file.delete()
        return Response('The file has been deleted successfully')
