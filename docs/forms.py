from django import forms


class UploadFileForm(forms.Form):
    projectname = forms.CharField(label='Project Name',max_length=15)
    axurefile = forms.FileField(label='zip files')

class EditFileForm(forms.Form):
    projectname = forms.CharField(label='Project Name',max_length=15)
    axurefile = forms.FileField(label='zip files',required=False)