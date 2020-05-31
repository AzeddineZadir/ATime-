from django.shortcuts import render
from .decorators import employe_required, manger_required, project_manger_required
from apps.pointage.models import Employe
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


@employe_required
def dash_emp(request):
    return render(request, 'dash/dash_emp.html')


@manger_required
def dash_man(request):
    # Get current user manager
    emp_man = Employe.objects.filter(user=request.user).get()
    # Get number of employe --> total/inside/outside
    print(emp_man.team)
    if emp_man.team != None:
        print("test")
        man_employe_stats = Employe.manager.get_my_employe_stats(team=emp_man.team, user_emp=request.user).get()
        team_name = emp_man.team.nom
    # Get all employe of current manager
        man_employe = Employe.manager.get_my_employe(team=emp_man.team, user_emp=request.user)
    else:
        man_employe_stats = None
        team_name = None
        man_employe = None

    return render(request, 'dash/dash_man.html', {'man_employe_stats':man_employe_stats, 'team_name':team_name, 'man_employe':man_employe})


@project_manger_required
def dash_pro_man(request):
    return render(request, 'dash/dash_pro_man.html', {'test':4})


def profile(request):
    return render(request, 'dash/profile.html')
