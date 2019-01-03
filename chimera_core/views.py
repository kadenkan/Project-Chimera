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
    chimera = Chimera()
    capt_text = chimera.create_random_captcha_text(4)
    captname = chimera.create_image_captcha(request, 1, capt_text)
    hashed_text = chimera.create_hash(capt_text)
    print(captname)

    if request.method == 'POST':
        data = request.POST.copy()

        if hashed_text == chimera.create_hash(data['imgtext']):
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)

            if user:

                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))

                else:
                    return render(request, 'chimera_core/login.html', {'inactive': True, 'tempname':  captname})

            else:
                print("Someone tried to login and failed.")
                print("They used username: {} and password: {}".format(
                    username, password))
                return render(request, 'chimera_core/login.html', {'loginerr': True, 'tempname':  captname})
        
        else:
            return render(request, 'chimera_core/login.html', {'ccerr': True, 'tempname':  captname})

    else:
        return render(request, 'chimera_core/login.html', {'tempname':  captname})
