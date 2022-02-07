from django.urls import path

from . import views

urlpatterns = [
    path('', views.celery_test, name='celery_test'),
]