from django.urls import path

from . import views

urlpatterns = [
    path('', views.rekognition_test, name='rekognition_test'),
]