from datetime import datetime

from django.http import JsonResponse, HttpResponseRedirect
from django.utils import timezone

from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404, render_to_response

# Create your views here.
from django.views.generic import UpdateView

from src.accounts.forms import UserForm, UserLoginForm, UserUpdateForm
from src.accounts.models import User


def login_view(request):  # users will login with their Email & Password
    if request.user.is_authenticated:
        return redirect("/")
    else:
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            # authenticate with Email & Password
            user = authenticate(email=email, password=password)
            login(request, user)
            return redirect("/")
        else:
            print(form.errors)
        return render(request, "accounts/login.html", {})


def register(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        errors = {}
        # gender = request.POST.get('gender')
        # name = request.POST.get('name')
        # email = request.POST.get('email')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        if password != confirm_password:
            errors["password"] = "Password should be matched"
            return render(request, 'accounts/register.html', errors)
        else:
            form = UserForm(request.POST or None)
            if form.is_valid():
                user = form.save(commit=False)
                password = form.cleaned_data.get("password1")
                user.set_password(password)
                user.save()
                return redirect('/')
            else:
                print(form.errors)
        return render(request, 'accounts/register.html')
    return render(request, 'accounts/register.html')


def logout_view(request):  # logs out the logged in users
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        user = get_object_or_404(User, email=request.user.email)
        user.updated_at = datetime.now(tz=timezone.utc)
        user.save()
        logout(request)
        return redirect("/")


@login_required(login_url='/login')
def profile_edit(request):
    if request.method == "POST":
        bio = request.POST['bio']
        country = request.POST['country']
        website = request.POST['website']
        form = UserUpdateForm(data=request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.bio = bio
            user.country = country
            user.website = website
            user.save()
            return JsonResponse({'success': 1})
        else:
            return JsonResponse(form.errors)
    return render(request, 'profile_edit.html', {})


def profile(request, username=None):
    user = User.objects.get(username=username)
    return render(request, 'profile.html', {'user': user, 'flag': 'tweet'})


@login_required(login_url='/login')
def settings_account(request):
    if request.method == "POST":
        form = UserUpdateForm(data=request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = request.POST['email']
            user.save()
            return render(request, 'accounts/account_update.html', {'user': request.user})
        else:
            print(form.errors)
    return render(request, 'accounts/account_update.html', {'user': request.user})


@login_required(login_url='/login')
def settings_password(request):
    if request.method == "POST":
        user = request.user
        current_password = request.POST['current_password']
        if user.check_password(current_password):
            new_password = request.POST['new_password']
            re_password = request.POST['re_password']
            if new_password == re_password:
                user.set_password('{}'.format(new_password))
                user.save()
                update_session_auth_hash(request, user)
                return redirect('/settings/password')
    return render(request, 'accounts/password_update.html', {'user': request.user})


@login_required(login_url='/login')
def upload_cover(request):
    photo = request.FILES['profileCover']
    user = get_object_or_404(User, email=request.user.email)
    user.profile_cover = photo
    user.save()
    return redirect('/profile/edit')


@login_required(login_url='/login')
def upload_profile(request):
    photo = request.FILES['profileImage']
    user = get_object_or_404(User, email=request.user.email)
    user.profile_picture = photo
    user.save()
    return redirect('/profile/edit')

# class AccountUpdateView(UpdateView):
#     model = User
#     template_name = 'accounts/account_update.html'
#     form_class = UserUpdateForm
#     context_object_name = 'user'
#
#     def get_object(self, queryset=None):
#         return self.request.user
#
#     def post(self, request, *args, **kwargs):
#         form = self.form_class(self.request.POST, self.request.user)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.email = self.request.POST['email']
#             user.save()
#             return HttpResponseRedirect('/settings/account')
#         else:
#             print(form.errors)
#         return render(request, self.template_name, {'form': form})

# @login_required(login_url="/login")
# def update_profile(request):
#     context = {
#         "user": request.user
#     }
#     if request.method == "GET":
#         return render(request, "profile/edit.html", context)
#     else:
#         about = request.POST['description']
#         looking_for = request.POST['looking_for']
#         interests = request.POST['interests']
#         city = request.POST['city']
#         country = request.POST['country']
#         user = get_object_or_404(User, email=request.user.email)
#         user.about = about
#         user.looking_for = looking_for
#         user.interests = interests
#         user.city = city
#         user.country = country
#         user.save()
#         return redirect('/profile/edit')
# 
# 
# @login_required(login_url="/login")
# def upload_profile_picture(request):
#     photo = request.FILES['photo']
#     user = get_object_or_404(User, email=request.user.email)
#     user.profile_picture = photo
#     user.save()
#     return redirect('/profile/edit')
