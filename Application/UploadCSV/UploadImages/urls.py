from django.urls import path
from . import views

urlpatterns = [
    path('upload_form/', views.show_upload_form, name='show_upload_form'),
    path('upload_csv/', views.uploadCSV, name='upload_csv'),
]