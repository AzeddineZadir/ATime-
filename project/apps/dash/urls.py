from django.urls import path, include
from . import views

app_name = 'dash'
urlpatterns = [
    path('dashboard_emp', views.dash_emp, name='employe_dashbored'),
    path('dashboard_man', views.dash_man, name='manager_dashbored'),
    path('dashboard_responsible', views.dash_responsible, name='responsible_dashbored'),
    path('profile', views.profile , name='profile'),
    path('profile/<str:pk>', views.view_profile , name='view_profile'),
    path('ma_fiche_pointage/<str:pk>', views.ma_fiche_pointage , name='ma_fiche_pointage'),
    path('fiche_pointage/', views.fiche_pointage , name='fiche_pointage'),
    path('mes_collaborateurs', views.mes_collaborateurs , name='mes_collaborateurs'),
    path('my_teams', views.my_teams , name='my_teams'),
    path('schedules', views.schedules , name='schedules'),
    path('schedule/<str:pk>', views.schedule , name='schedule'),
    path('modify_schedule/<str:pk>', views.modify_schedule , name='modify_schedule'),
    path('assign_schedule/<str:pk>', views.assign_schedule , name='assign_schedule'),
    path('create_schedule', views.create_schedule , name='create_schedule'),
    path('delete_schedule/<str:pk>', views.delete_schedule , name='delete_schedule'),
    path('delete_employe_schedule/<str:pk>', views.delete_employe_schedule , name='delete_employe_schedule'),
    path('create_team', views.create_team , name='create_team'),
    path('assign_team/<str:pk>', views.assign_team , name='assign_team'),
    path('modify_team/<str:pk>', views.modify_team , name='modify_team'),
    path('delete_team/<str:pk>', views.delete_team , name='delete_team'),
    path('delete_employe_team/<str:pk>', views.delete_employe_team , name='delete_employe_team'),
    path('mes_employes', views.mes_employes , name='mes_employes'),
    path('fiche_pointage_all/', views.fiche_pointage_all , name='fiche_pointage_all'),
    
]
