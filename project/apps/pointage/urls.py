from django.urls import path, include
from . import views

app_name = 'pointage'
urlpatterns = [
    # path('check', views.check),
    path('getid', views.getid),
    path('dashboard_emp', views.dash, name='dash_emp'),
    path('dashboard_man', views.dash_man, name='dash_proman'),
    path('dashboard_pro_man', views.dash_man, name='dash_pro_man'),
]
