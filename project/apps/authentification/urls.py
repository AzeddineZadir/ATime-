from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='authentification/login.html'), name='login'),
    path('dashborad/', views.dash, name='dash'),
    path('logout/', auth_views.LogoutView.as_view(template_name='authentification/login.html'), name='logout'),
]