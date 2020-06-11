from django.urls import path, include
from . import views

app_name = 'dash'
urlpatterns = [
    path('dashboard_emp', views.dash_emp, name='employe_dashbored'),
    path('dashboard_man', views.dash_man, name='manager_dashbored'),
    path('dashboard_pro_man', views.dash_pro_man, name='project_manager_dashbored'),
    path('profile', views.profile , name='profile'),
    path('profile/<str:pk>', views.view_profile , name='view_profile'),
    path('ma_fiche_pointage/<str:pk>', views.ma_fiche_pointage , name='ma_fiche_pointage'),
    path('fiche_pointage/', views.fiche_pointage , name='fiche_pointage'),
    path('mes_collaborateurs', views.mes_collaborateurs , name='mes_collaborateurs'),
]
