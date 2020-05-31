from django.urls import path, include
from . import views

app_name = 'dash'
urlpatterns = [
    path('dashboard_emp', views.dash_emp, name='employe_dashbored'),
    path('dashboard_man', views.dash_man, name='manager_dashbored'),
    path('dashboard_pro_man', views.dash_pro_man, name='project_manager_dashbored'),
    path('profile', views.profile , name='profile'),
]
