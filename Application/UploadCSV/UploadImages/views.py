from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User, File, UploadedImage
from datetime import datetime
from django.core.files.storage import default_storage
import csv


# Entry View for the User to be able to see de upload form
# This view is protected by the login_required decorator, which means that only authenticated users can access it.
@login_required
def show_upload_form(request):
    user = request.user
    context = {'user': user}
    return render(request, 'Upload/upload_form.html', context)

# This view gets the file and al the POST data fromthe form, and saves the file in the Uploads folder.
# It also creates a File object in the database with the file name, user, status and file path.
@login_required
def uploadCSV(request):
    if request.method == 'POST':
        current_dateTime = datetime.now()
        user = User.objects.get(id=request.POST['username'])
        fecha = str(current_dateTime.year) + str(current_dateTime.month) + str(current_dateTime.day)
        uploaded_file = request.FILES['file']
        filename = user.username+fecha+uploaded_file.name
        Archivo = File.objects.create(
            fileName=filename,
            user=user,
            status='pending',
            filePath="Uploads/"+filename,
        )
        try:
            default_storage.save(filename, uploaded_file)
            Archivo.status = 'successful' # Update the status to 'successful' after saving the file
            Archivo.save()
            imagesProcesed = processListofImages(request, filename, Archivo)
            for image in imagesProcesed:
                print(image.name)

        except Exception as e:
            print(f"Error saving file: {e}")
            Archivo.status = 'failed' #update the status to 'failed' if there was an error
            Archivo.save()
            return render(request, 'Upload/upload_fileError.html')
        return render(request, 'Upload/upload_success.html', {'file_name': uploaded_file.name, 'lista': imagesProcesed})
    return render(request, 'Upload/upload_form.html')

#This function gets the file and processes it to create an UploadedImage for each line in the file.
@login_required
def processListofImages(request, fileName, Archivo):
    files = list()
    try:
        ArchivodeStrorage = default_storage.open(fileName)
        with open(ArchivodeStrorage.name, 'r') as csvfile:
            csv.reader(ArchivodeStrorage)
            next(csvfile) #Skip Headers
            for row in csvfile:
                line = row.split(",")
                if len(line) > 0:
                    Imagen = UploadedImage.objects.create(
                        file=Archivo,
                        name=str(line[0]).strip(),
                        description=str(line[1]).strip(),
                        image=str(line[2]).strip(),
                        image_path="Uploads/",
                        status='pending',
                    )
                   
                    try:
                        Imagen.status = 'successful' # Update the status to 'successful' after saving the image
                        Imagen.save()                        
                    except Exception as e:
                        Imagen.status = 'failed' #upadate the status to 'failed' if there was an error
                        Imagen.save()
                    files.append(Imagen)
                    
            return files
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        Imagen.status = 'failed'
        Archivo.save()
        return render(request, 'Upload/upload_fileError.html')