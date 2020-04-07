from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User

from accounts.forms import RegistrationFormUniqueEmail, LoginForm, UserEditForm, ProfileEditForm


class LoginView(View):
    """ Login """
    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(
                request, username=cd["username"], password=cd["password"]
            )
            if user is None:
                return HttpResponse("Invalid login")

            if not user.is_active:
                return HttpResponse("Disabled account")

            login(request, user)
            messages.success(request, "Добро пожаловать, вы зарегистрированы")
            return HttpResponse("Welcome! Authenticated successfully")
        else:
            return render(request, "accounts/login.html", {"form": form})

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, "accounts/login.html", {"form": form})


def register(request):
    """ User registration """
    if request.method == "POST":
        form = RegistrationFormUniqueEmail(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data["password"])
            new_user.save()

            return render(
                request, "accounts/registration_complete.html",
                {"new_user": new_user}
            )
    else:
        form = RegistrationFormUniqueEmail()

    return render(request, "accounts/register.html", {"user_form": form})


@login_required
def profile(request):
    """ Get user-profile page"""
    if request.method == "POST":
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(
            instance=request.user.profile, data=request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Профиль изменен")
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)

    return render(
        request,
        "accounts/edit.html",
        {"user_form": user_form, "profile_form": profile_form},
    )


@login_required
def menu(request):
    return render(request, 'menu.html')


class DeleteProfile(View):
    """ Delete profile """
    def post(self, request, *args, **kwargs):
        user = request.user
        profile = User.objects.filter(id=user.id)
        profile.delete()
        return render(request, "profile-deleted.html")

    def get(self, request, *args, **kwargs):
        return render(request, "accounts/delete-profile.html")
