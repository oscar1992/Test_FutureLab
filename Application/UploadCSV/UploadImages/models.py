from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fileName = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    filePath = models.CharField(max_length=255)
    file = models.FileField(upload_to='Uploads/')
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('failed', 'Failed'), ('successful', 'Successful')], default='pending')

    def __str__(self):
        return f"{self.user.username} - {self.fileName}"
    
class UploadedImage(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=100)
    description = models.TextField()
    image_path = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('failed', 'Failed'), ('successful', 'Successful')], default='pending')

    def __str__(self):
        return f"{self.name} - {self.image}"
    
