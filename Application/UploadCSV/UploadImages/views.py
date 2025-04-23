from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User, File, UploadedImage
from datetime import datetime
from django.core.files.storage import default_storage
import csv

# Create your views here.
@login_required
def show_upload_form(request):
    user = request.user
    context = {'user': user}
    return render(request, 'Upload/upload_form.html', context)

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
            Archivo.status = 'successful'
            Archivo.save()
            imagesProcesed = processListofImages(request, filename, Archivo)
            for image in imagesProcesed:
                print(image.name)

        except Exception as e:
            print(f"Error saving file: {e}")
            Archivo.status = 'failed'
            Archivo.save()
            return render(request, 'Upload/upload_fileError.html')
        return render(request, 'Upload/upload_success.html', {'file_name': uploaded_file.name, 'lista': imagesProcesed})
    return render(request, 'Upload/upload_form.html')

@login_required
def processListofImages(request, fileName, Archivo):
    files = list()
    try:
        ArchivodeStrorage = default_storage.open(fileName)
        with open(ArchivodeStrorage.name, 'r') as csvfile:
            csv.reader(ArchivodeStrorage)
            next(csvfile) #Omitir Headers
            for row in csvfile:
                line = row.split(",")
                if len(line) > 0:
                    print(str(line[0]).strip())
                    print(str(line[1]).strip())
                    print(str(line[2]).strip())
                    Imagen = UploadedImage.objects.create(
                        file=Archivo,
                        name=str(line[0]).strip(),
                        description=str(line[1]).strip(),
                        image=str(line[2]).strip(),
                        image_path="Uploads/",
                        status='pending',
                    )
                    print(Imagen.name)
                    try:
                        Imagen.status = 'successful'
                        Imagen.save()                        
                    except Exception as e:
                        Imagen.status = 'failed'
                        Imagen.save()
                    files.append(Imagen)
                    print("Imagen: " + str(Imagen.name))
            return files
    except Exception as e:
        print(f"Error processing CSV file: {e}")
        Imagen.status = 'failed'
        Archivo.save()
        return render(request, 'Upload/upload_fileError.html')