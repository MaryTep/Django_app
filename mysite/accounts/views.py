from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.http import HttpRequest, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LogoutView
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView
from django.utils.translation import gettext_lazy as _, ngettext

from .models import Profile, User


class HelloWorldView(View):
    welcome_message = _("Welcome Hello world!")

    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET.get('items') or 0
        items = int(items_str)
        products_line = ngettext(
            "one product",
            "{count} products",
            items
        )
        products_line = products_line.format(count=items)
        return HttpResponse(
            f"<h1>{self.welcome_message}</h1>"
            f"\n<h2>{products_line}</h2>"
        )

# def login_view(request: HttpRequest):
#     if request.method == "GET":
#         if request.user.is_authenticated:
#             return redirect('/admin/')
#         return render(request, 'accounts/login.html')
# 
#     username = request.POST["username"]
#     password = request.POST["password"]
# 
#     user = authenticate(request, username=username, password=password)
#     if user is not None:
#         login(request, user)
#         return redirect('/admin/')
# 
#     return render(request, 'accounts/login.html', {"error": "Invalid login credentials"})
# 
# 
# def logout_view(request: HttpRequest):
#     logout(request)
#     return redirect(reverse("accounts:login"))
# 
# 
class MyLogoutView(LogoutView):
    next_page = reverse_lazy("accounts:login")


# class AboutMeView(TemplateView):
#     template_name = "accounts/about-me.html"
#     model = Profile
#     context_object_name = "profile"
#
    # def get_success_url(self):
    #     return reverse(
    #         "accounts:about_me",
    #         kwargs={"pk": self.object.pk},
    #     )


class UsersListView(ListView):
    template_name = 'accounts/users-list.html'
    context_object_name = "users"
    queryset = User.objects.select_related('profile')
    # queryset = Product.objects.filter(archived=False)


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:about_me')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password1")

        user = authenticate(self.request, username=username, password=password)
        login(request=self.request, user=user)
        return response

    # def get_success_url(self):
    #     return reverse(
    #         "accounts:about_me",
    #         kwargs={"pk": self.object.pk},
    #     )


class UpdateProfileView(UpdateView):
    model = Profile
    fields = "user", "bio", "avatar"
    # form_class = ProfileForm
    template_name_suffix = "_update_form"

    # def form_valid(self, form):
    #     response = super().form_valid(form)
    #     for avatar in form.files.get():
    #         Profile.objects.create(
    #             user=self.object,
    #             avatar=avatar,
    #         )
    #     return response

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        user = User.objects.select_related("profile").get(pk=pk)
        try:
            return user.profile
        except Profile.DoesNotExist:
            return Profile.objects.create(user=user)

    def get_success_url(self):
        return reverse(
            "accounts:about_user",
            kwargs={"pk": self.kwargs.get(self.pk_url_kwarg)},
        )


class AboutMeView(UpdateView):
    template_name = "accounts/about-me.html"
    model = Profile
    fields = "bio", "avatar",

    success_url = reverse_lazy("accounts:about_me")

    def get_object(self, queryset=None):
        return self.request.user.profile


class AboutUserView(DetailView):
    template_name = "accounts/about-user.html"
    model = User
    queryset = User.objects.select_related("profile")
    context_object_name = "user"

    success_url = reverse_lazy("accounts:about_user")
