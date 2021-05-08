from django.shortcuts import redirect, render, reverse

from .forms import InputForm
from .models import InputModel, Validation
from django.core.files.storage import FileSystemStorage


import xml.etree.ElementTree as ET
import os.path

#--------------------------------------------------------------------------------------------------------------------
#               Issues to be fixed
#1) Edit Results Table to Output text found in the XML , no more PASS/FAIL
#   - 
#--------------------------------------------------------------------------------------------------------------------
#               Things to do
#1)Test on AWS servers
#2)Filepath is not xml document -> return "Upload right document"
#   - Don't upload file when not xml
#   - Delete file from server once complete?
#3)Edit home screen with instructions
#   - Last thing learn CSS to style webpage
#4)Export Results Table into .csv or other sort of file
#   - Proctors have report to download quickly
#5)Build out rest of criteria/Cures updates
#--------------------------------------------------------------------------------------------------------------------

# Create your views here.
def inputs(request):
    if request.method == 'POST':
        InputModel.objects.all().delete()
        form = InputForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('results')
    else:
        form = InputForm()
    return render(request, "Inputs/inputs.html", {
        'form':form,
    })

def results(request):
    uploads = InputModel.objects.all()
    crit = uploads[0].criteria

    path_string = uploads[0].filename
    text = str(path_string)
    file_type = text[-4:]
    if file_type != '.xml':
        print('ERROR')
        return redirect('inputs')    #Needs alert to import correct file
    else:
        filepath = f'.//media/{uploads[0].filename}'
        validation = Validation(crit,filepath)

    
    return render(request, "Inputs/results.html", {
        'uploads': uploads,
        'validation': validation
    })