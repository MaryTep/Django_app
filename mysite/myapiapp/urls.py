from django.urls import path

# from CBV.mysite.mysite.urls import urlpatterns
from .views import hello_world_new, GroupsListView

appname = "myapiapp"

urlpatterns = [
    path('hello/', hello_world_new, name='hello'),
    path('groups/', GroupsListView.as_view(), name='groups'),
]