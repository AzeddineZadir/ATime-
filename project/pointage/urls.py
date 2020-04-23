from django.urls import path, include
from . import views

urlpatterns = [
    # path('check', views.check),
    path('getid', views.getid),
]
