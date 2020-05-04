from django.urls import path, include
from . import views

app_name = 'pointage'
urlpatterns = [
    # path('check', views.check),
    path('getid', views.getid),
    path('test', views.test),

]
