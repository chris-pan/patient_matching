from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import UploadFileForm
from django.core.files.storage import FileSystemStorage
from .something import handle_uploaded_file
from .main import main
 


# Imaginary function to handle an uploaded file.
# from somewhere import handle_uploaded_file
def index(request):
    return render(request, 'matching/matching.html')

def upload(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        print("CHARSET", uploaded_file.charset)
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
        # print(uploaded_file.path)
        # print(request.FILES['document'].temporary_file_path())
        # print(uploaded_file.name)
        # call function 
        main(uploaded_file)
        
    return render(request, 'matching/upload.html')
