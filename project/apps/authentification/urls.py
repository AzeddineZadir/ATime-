from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.Login.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authentification/login.html'), name='logout'),
]