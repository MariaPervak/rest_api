import os
from threading import Thread
from queue import Queue

from rest_api.serializers import FilesDataSerializers

class Uploader(Thread):

    def __init__(self, queue, name, path_to_upload, path_uploaded):
        Thread.__init__(self)
        self.name = name
        self.path_to_upload = path_to_upload
        self.path_uploaded = path_uploaded
        self.queue = queue

    def run(self):
        while True:
            file = self.queue.get()
            self.upload_file(file)
            self.queue.task_done()

    def upload_file(self, file):
        
        with open(self.path_to_upload + file, 'rb') as f:
            data = f.read()
        with open(self.path_uploaded + file, 'wb') as f:
            f.write(data)

        dfile = FilesDataSerializers(data={'image_path' : file})
        if dfile.is_valid(raise_exception=True):
            dfile.save()

        msg = "%s закончил загрузку %s" % (self.name, file)
        print(msg)
