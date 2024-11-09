from django.urls import path
from .views import process_get_view, user_form, handle_file_upload, spam_page

app_mame = 'requestdataapp'
urlpatterns = [
    path('get/', process_get_view, name='get-view'),
    path('bio/', user_form, name='user-form'),
    path('upload/', handle_file_upload, name='file-upload'),
    path('spam/', spam_page, name='spam-page'),
]
