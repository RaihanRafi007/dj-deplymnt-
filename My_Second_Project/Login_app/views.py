from django.contrib import auth
from django.shortcuts import render, redirect
from Login_app.forms import UserForm, UserInfoForm
from Login_app.models import UserInfo
from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib import messages
# Create your views here.

def login_page(request):
    if request.user.is_authenticated:
		    return redirect('Login_app:home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('Login_app:home')
           
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'Login_app/login.html', context)

@login_required
def logoutUser(request):
	logout(request)
	return redirect('Login_app:login')


def home(request):
    dict = {}
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id
        user_basic_info = User.objects.get(pk=user_id)
        user_more_info = UserInfo.objects.get(user__pk=user_id)
        dict = {'user_basic_info': user_basic_info, 'user_more_info': user_more_info}
    return render(request, 'Login_app/index.html', context=dict)

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_info_form = UserInfoForm(data=request.POST)

        if user_form.is_valid() and user_info_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            user_info = user_info_form.save(commit=False)
            user_info.user = user

            if 'profile_pic' in request.FILES:
                user_info.profile_pic = request.FILES['profile_pic']

            user_info.save()

            registered = True

    else:
        user_form = UserForm()
        user_info_form = UserInfoForm()

    dict = {'user_form': user_form, 'user_info_form': UserInfoForm, 'registered': registered}
    return render(request, 'Login_app/register.html', context=dict)



