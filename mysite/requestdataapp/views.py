from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.core.files.storage import FileSystemStorage

from .for_validate.for_validate import validate_file_size
from .forms import UserBioForm, UploadFileForm


def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get("a", "")
    b = request.GET.get("b", "")
    result = a + b
    context = {
        "a": a,
        "b": b,
        "result": result,

    }
    return render(request, 'requestdataapp/request-query-params.html', context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    context = {
        "form": UserBioForm()
    }
    return render(request, 'requestdataapp/user-bio-form.html', context=context)


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    """ 5 Mb = 5 * 1024 *1024 """
    MAX_UPLOAD_SIZE = 5242880

    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            myfile = form.cleaned_data["file"]
            big_file = validate_file_size(myfile.size, MAX_UPLOAD_SIZE)
            context = {
                'big_file': big_file,
                'form': form
            }
            if big_file:
                return render(request, 'requestdataapp/file-upload.html', context=context)

            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            print("Сохраненный файл", filename)
            context = {
                'big_file': 'Файл сохранен',
                "form": form
            }
            return render(request, 'requestdataapp/file-upload.html', context=context)
        else:
            context = {
                'form': form
            }
            return render(request, 'requestdataapp/file-upload.html', context=context)

    context = {
        "form": UploadFileForm()
    }
    return render(request, 'requestdataapp/file-upload.html', context=context)


def spam_page(request: HttpRequest) -> HttpResponse:
    context = {
    }
    return render(request, 'requestdataapp/spam-page.html', context=context)


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    print(ip)
    return ip
