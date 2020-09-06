from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from apps.dash.views import dash_emp, dash_man, dash_responsible
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User

from django.contrib.auth import (
    authenticate,
    login,
    logout
)
from .forms import UserLoginForm

# Create your views here.


class Login(LoginView):
    template_name = 'authentification/login.html'

    def get_success_url(self):  # if username and password are correct
        role = self.request.user.role

        if role == 1:
            print("Je suis un employé")
            return reverse('dash:employe_dashbored')
        elif role == 2:
            print("Je suis un manager")
            return reverse('dash:manager_dashbored')
        elif role == 3:
            print("Je suis un chef de projet")
            return reverse('dash:responsible_dashbored')
        else:
            print("Je suis abehri")


@login_required(redirect_field_name='login')  # Require auth
def dash(request):  # Check role of user
    role = request.user.role
    if role == 1:
        print("Employe")
        html = "<html><body>Employe</body></html>"
        return HttpResponse(html)
    elif role == 2:
        print("Manager")
        html = "<html><body>Manager</body></html>"
        return HttpResponse(html)
    elif role == 3:
        print("Chef de projet")
        html = "<html><body>Chef de projet</body></html>"
        return HttpResponse(html)
    else:
        raise Http404("Not Found")



def login_view(request):
    next = request.GET.get('next')
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        login(request, user)
        role = user.role
        print('tttttt')

        if role == 1:
            print("Je suis un employé")
           
            return redirect(reverse('dash:employe_dashbored')) 
        elif role == 2:
            print("Je suis un manager")
            return redirect(reverse('dash:manager_dashbored'))
        elif role == 3:
            print("Je suis un chef de projet")
            return redirect(reverse('dash:responsible_dashbored'))
        else:
            print("Je suis abehri")
        return redirect('/')   
    context = {
        'form' : form,
    }
    return render(request, "authentification/login.html", context)