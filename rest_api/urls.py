from django.urls import path
from rest_api.views import *

urlpatterns = [
    path('files/', Files.as_view()),
    path('files/<int:pk>', Files.as_view()),
    path('files/post', Files.as_view())
]
