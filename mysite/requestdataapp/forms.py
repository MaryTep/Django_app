from django import forms
from django.core.validators import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
#from requestdataapp.for_validate.for_validate import validate_0_100


class UserBioForm(forms.Form):
    name = forms.CharField(max_length=100)
    age = forms.IntegerField(label="Ваш возраст", min_value=0, max_value=100)
    bio = forms.CharField(label="Биография", widget=forms.Textarea)


def validate_file_name(file: InMemoryUploadedFile) -> None:
    if file.name and ('virus' in file.name.lower()):
        raise ValidationError('File name should not contain `virus`')


class UploadFileForm(forms.Form):
    file = forms.FileField(validators=[validate_file_name])
