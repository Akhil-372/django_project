from django.urls import path
from . import views

app_name='image_classifier'

urlpatterns = [
    path('',views.index,name='index'),
    path('upload/',views.upload_file,name='upload'),
]
