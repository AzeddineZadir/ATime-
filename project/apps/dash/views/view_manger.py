from django.shortcuts import render, HttpResponseRedirect
from apps.dash.decorators import employe_required, manger_required, project_manger_required
from django.contrib.auth.decorators import login_required
from apps.pointage.models import Employe, User, Planing, Shift
from django.core.exceptions import ObjectDoesNotExist
from apps.dash.forms import UserForm
from django.urls import reverse
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.utils import timezone
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q


@manger_required
def dash_man(request):
    # Get current user manager
    emp_man = Employe.objects.filter(user=request.user).get()
    # Get number of employe --> total/inside/outside
    print(emp_man.team)
    if emp_man.team != None:
        man_employe_stats = Employe.manager.get_my_employe_stats(
            team=emp_man.team, user_emp=request.user).get()
        team_name = emp_man.team.nom
    # Get all employe of current manager
        man_employe = Employe.manager.get_my_employe(
            team=emp_man.team, user_emp=request.user)
    else:
        man_employe_stats = None
        team_name = None
        man_employe = None

    return render(request, 'dash/dash_man.html', {'man_employe_stats': man_employe_stats, 'team_name': team_name, 'man_employe': man_employe})
