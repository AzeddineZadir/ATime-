from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User


# Create your views here.

class Login(LoginView):
    template_name = 'authentification/login.html' 

    def get_success_url(self): # if username and password are correct
        role = self.request.user.role   

        if role == 1:
            print("Je suis un employé")
        elif role == 2:
            print("Je suis un manager")
        elif role == 3:
            print("Je suis un chef de projet")
        else:
            print("Je suis abehri")
