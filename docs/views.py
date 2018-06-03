from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm,EditFileForm

from .models import Doc
from .filehandler import handle_uploaded_file,handle_filedir

import os,shutil,time
from pathlib import Path


# Create your views here.

def home(request):
    return render(request, 'docs/index.html')


@login_required
def docs(request):
    docs_owner = request.user
    docs = Doc.objects.filter(owner=docs_owner)
    return render(request, 'docs/docs.html',{'docs':docs})


@login_required
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = Doc()
            file.name = form.cleaned_data['projectname']
            file.owner = request.user
            file.fileLocation = 'sample'
            file.fileUrl = 'sample'
            file.save()

            username = request.user.username
            now = str(int(time.time()))
            username_now_name = username + now

            filedirname = handle_filedir(username_now_name)

            file_number = str(file.id)

            file.fileLocation = handle_uploaded_file(request.FILES['axurefile'],file_number,filedirname)
            file.fileUrl = os.path.join(str(file_number),filedirname,'index.html')

            file.save()

            return HttpResponseRedirect('/docs/')
    else:
        form = UploadFileForm()
    return render(request, 'docs/upload.html', {'form': form})

@login_required
def delete(request,id):
    doc = Doc.objects.get(id=id)
    if doc.owner == request.user:
        doc.delete()
        shutil.rmtree(doc.fileLocation)
    return HttpResponseRedirect('/docs/')


@login_required
def edit(request,id):
    doc = Doc.objects.get(id=id)
    if doc.owner == request.user:
        if request.method == 'POST':
            form = EditFileForm(request.POST, request.FILES)
            if form.is_valid():
                doc.name = form.cleaned_data['projectname']

                if 'axurefile' in request.FILES:
                    filedirname = doc.fileUrl.split('/')[1]
                    while Path(doc.fileLocation).is_dir():
                        shutil.rmtree(doc.fileLocation)

                    file_number = str(doc.id)

                    doc.fileLocation = handle_uploaded_file(request.FILES['axurefile'], file_number, filedirname)
                    doc.fileUrl = os.path.join(str(file_number), filedirname, 'index.html')

                doc.save()

                return HttpResponseRedirect('/docs/')
        else:
            data = {'projectname':doc.name}
            form = EditFileForm(data)

        return render(request, 'docs/edit.html', {'form': form,'doc':doc})
