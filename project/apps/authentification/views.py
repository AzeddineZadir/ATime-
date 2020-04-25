from django.shortcuts import render
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import Http404


# Create your views here.

@login_required(redirect_field_name='login') # Require auth
def dash(request): # Check role of user
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
 
        
    



