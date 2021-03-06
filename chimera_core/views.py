from django.conf import settings
from django.shortcuts import render
from chimera_core.forms import UserRegForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from chimera_core.models import Chimera
from .backend import ChimeraAuthBackend


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

        chimera = Chimera.objects.get(id=request.session['chimera'])

        cab = ChimeraAuthBackend()

        username = request.POST.get('username')

        chimerapw = request.POST.get('chimerapw')

        if cab.validate(chimera, chimerapw):

            try:
                user = authenticate(chimera=chimera, username=username, chimerapw=chimerapw)

            except:
                return render(request, 'chimera_core/login.html', {'loginerr': True})

            if user:

                if user.is_active:

                    login(request, user)

                    user.save()

                    return HttpResponseRedirect(reverse('index'))

                else:

                    return render(request, 'chimera_core/login.html', {'inactive': True})

            else:

                print("Someone tried to login and failed.")

                print("They used username: {} and password: {}".format(
                    username, chimerapw))

                return render(request, 'chimera_core/login.html', {'loginerr': True})

        else:

            return render(request, 'chimera_core/login.html', {'ccerr': True})

    else:

        return render(request, 'chimera_core/login.html')


def login_form(request):

    chimera = Chimera()

    chimera.generate_chimera_codes(request)

    chimera.save()

    ccnames = chimera.tempname_list

    request.session['chimera'] = chimera.id

    return render(request, 'chimera_core/login.html', {'tempnames':  ccnames})
