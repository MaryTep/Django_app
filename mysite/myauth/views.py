from random import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.urls import reverse, reverse_lazy
from django.views import View
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView, CreateView
from django.views.decorators.cache import cache_page

#from .models import Profile_myauth


def login_view(request: HttpRequest):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/admin/')
        return render(request, 'myauth/login.html')

    username = request.POST["username"]
    password = request.POST["password"]

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/admin/')

    return render(request, 'myauth/login.html', {"error": "Invalid login credentials"})


def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse("myauth:login"))


class MyLogoutView(LogoutView):
    next_page = reverse_lazy("myauth:login")


def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse("cookie set")
    response.set_cookie("fizz", "buzz", max_age=3600)
    return response


@cache_page(60 * 2)
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get("fizz", "default_value")
    return HttpResponse(f"Cookie value: {value!r} + {random()}")


@permission_required("myauth.view_profile", raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session["foobar"] = "spameggs"
    return HttpResponse("Session set")


@login_required()
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get("foobar", "default_value")
    return HttpResponse(f"Session value: {value!r}")


class AboutMeView(TemplateView):
    template_name = "myauth/about-me.html"


# class RegisterView(CreateView):
#     form_class = UserCreationForm
#     template_name = 'myauth/register.html'
#     success_url = reverse_lazy('myauth:about-me')
#
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         Profile_myauth.objects.create(user=self.object)
#
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password1")
#         print(username, password)
#
#         user = authenticate(self.request, username=username, password=password)
#         login(request=self.request, user=user)
#         return response


class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})
