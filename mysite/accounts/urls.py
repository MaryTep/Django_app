from django.urls import path
from django.contrib.auth.views import LoginView

from .views import (
                    MyLogoutView,
                    AboutMeView,
                    RegisterView,
                    UsersListView,
                    UpdateProfileView,
                    AboutUserView,
                    HelloWorldView,

)

app_mame = 'accounts'
urlpatterns = [
    path('login/',
         LoginView.as_view(template_name="accounts/login.html", redirect_authenticated_user=True),
         name='login'
         ),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path("register/", RegisterView.as_view(), name="register"),
    path("users-list/", UsersListView.as_view(), name="users_list"),
    path("about-me/", AboutMeView.as_view(), name="about_me"),
    # path("about-me/profile_update_form/", UpdateProfileView.as_view(), name="profile_update_form"),
    path("about-user/<int:pk>/", AboutUserView.as_view(), name="about_user"),
    path("about-user/<int:pk>/profile_update_form/", UpdateProfileView.as_view(), name="profile_update_form"),
    path("hello/", HelloWorldView.as_view(), name="hello")
]
