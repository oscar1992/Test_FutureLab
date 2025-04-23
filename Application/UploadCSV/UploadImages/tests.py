from django.test import TestCase
from .models import File, UploadedImage, User
# Create your tests here.

class FileModelTest(TestCase):
    def testFile(self):
        self.user = User.objects.create(username='testuser', email='email@test.com', password='password')
        self.file = File.objects.create(
            user=self.user,
            fileName='testfile.csv',
            filePath='Uploads/testfile.csv',
            status='pending'
        )
        self.uploaded_image = UploadedImage.objects.create(
            file=self.file,
            name='testimage',
            image='testimage.jpg',
            description='Test image description',
            image_path='Uploads/testimage.jpg',
            status='pending'
        )
        try:
            self.file.save()            
        except Exception as e:
            print(f"Error saving file: {e}")
            self.file.status = 'failed'

        self.assertEqual(self.file.status, 'pending')

class UploadedImageModelTest(TestCase):
        def testImage(self):
            self.user = User.objects.create(username='testuser', email='email@test.com', password='password')
            self.file = File.objects.create(
                user=self.user,
                fileName='testfile.csv',
                filePath='Uploads/testfile.csv',
                status='pending'
            )
            self.uploaded_image = UploadedImage.objects.create(
                file=self.file,
                name='testimage',
                image='testimage.jpg',
                description='Test image description',
                image_path='Uploads/testimage.jpg',
                status='pending'
            )
            try:
                self.uploaded_image.save()            
            except Exception as e:
                print(f"Error saving Image: {e}")
                self.uploaded_image.status = 'failed'

            self.assertEqual(self.file.status, 'pending')

class UserModelTest(TestCase):
    def testUser(self):
            self.user = User.objects.create(username='testuser', email='email@test.com', password='password')
            try:
                self.user.save()            
            except Exception as e:
                print(f"Error saving file: {e}")

            userDB = User.objects.get(username='testuser')
            self.assertEqual(userDB.username, 'testuser')
