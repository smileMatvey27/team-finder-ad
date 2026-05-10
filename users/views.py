from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from candf.constants import LOGIN_ERROR
from candf.functions import paginate_queryset
from users.forms import ChangePasswordForm, EditProfileForm, LoginForm, RegisterForm

from .models import User


def user_list(request):
    participants = User.objects.all().order_by("-id")
    page = paginate_queryset(request, participants)
    return render(request, "users/participants.html", {"participants": page})


def user_details(request, user_id):
    user = get_object_or_404(User, id=user_id)
    return render(request, "users/user-details.html", {"user": user})


def user_register(request):
    form = RegisterForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        if not user.avatar:
            user.generate_avatar()
        user.save()
        login(request, user)
        return redirect("projects:project_list")
    return render(request, "users/register.html", {"form": form})


def user_login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect("projects:project_list")
        form.add_error(None, LOGIN_ERROR)
    return render(request, "users/login.html", {"form": form})


@login_required
def user_edit_profile(request):
    form = EditProfileForm(
        request.POST or None, request.FILES or None, instance=request.user
    )
    if form.is_valid():
        form.save()
        return redirect("users:user_detail", user_id=request.user.id)
    return render(request, "users/edit_profile.html", {"form": form})


@login_required
def user_change_password(request):
    form = ChangePasswordForm(request.user, request.POST or None)
    if form.is_valid():
        user = request.user
        user.set_password(form.cleaned_data["new_password1"])
        user.save()
        update_session_auth_hash(request, user)
        return redirect("users:user_detail", user_id=user.id)
    return render(request, "users/change_password.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("projects:project_list")
