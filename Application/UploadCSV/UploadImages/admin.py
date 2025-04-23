from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import User, File, UploadedImage

# Register your models here.
CustomUser = get_user_model()

admin.site.register(CustomUser)
admin.site.register(File)
admin.site.register(UploadedImage)