from django.shortcuts import render, render_to_response
from chimera_core.forms import UserRegForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from chimera_core.core import Chimera


def index(request):
    return render(request, 'chimera_core/index.html')


@login_required
def special(request):
    return HttpResponse("You are logged in !")


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    registered = False
    if request.method == 'POST':
        regform = UserRegForm(data=request.POST)
        if regform.is_valid():
            user = regform.save()
            user.set_password(user.password)
            user.save()
            registered = True
        else:
            print(regform.errors)
    else:
        regform = UserRegForm()
    return render(request, 'chimera_core/registration.html',
                  {'form': regform,
                   'registered': registered})


def user_login(request):
    if request.method == 'POST':
        image = Chimera.create_image_captcha(request,1,)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(
                username, password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'chimera_core/login.html', {})
