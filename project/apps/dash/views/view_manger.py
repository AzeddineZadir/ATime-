from django.shortcuts import render, HttpResponseRedirect
from apps.dash.decorators import employe_required, manger_required, responsible_required
from django.contrib.auth.decorators import login_required
from apps.pointage.models import Employe, User, Planing, Shift, Team
from django.core.exceptions import ObjectDoesNotExist
from apps.dash.forms import UserForm, TeamForm
from django.urls import reverse
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.utils import timezone
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.dash.views import get_now_t, convert_time, is_valid, hours_dif, get_laste_entry, get_inpost_t, get_time_left
from django.db.models import Q


def get_coleagues(employe,managed_teams):
    
    #print(f"in get coleagues {managed_teams}")
    coleagues=Employe.objects.filter(team__in=managed_teams)
    #coleagues_nbr=coleagues.count()
    #print(f"in get coleagues {coleagues_nbr}")
    return coleagues
def get_employes(team, ):
    # get the employes of the team in
    colaborators = Employe.objects.filter(team=team,)
    return colaborators


def get_employes_by_presence(team, iwssad):
    # get the employes of the team in
    colaborators = Employe.objects.filter(team=team, iwssad=iwssad)
    return colaborators


@manger_required
def dash_man(request):
    # Get employe with id
    man = Employe.objects.filter(user=request.user).get()
    # the employe dash boreed part

    shift = man.get_last_shift()
    he = get_laste_entry(shift)
    now = get_now_t()
    in_post_t = get_inpost_t(man)
    time_left = get_time_left(man)
    try:
        t_h = man.get_today_hours()
        todays_hours = [t_h.he1, t_h.hs1, t_h.he2, t_h.hs2, ]
    except:
        todays_hours = ['H:M', 'H:M', 'H:M', 'H:M']

    managed_teams =man.managed_team.all()
    managed_teams_nbr=managed_teams.count()
    collaborateurs = get_coleagues(man,managed_teams)
    if (collaborateurs):

        for col in collaborateurs:
            shift=col.get_last_shift()
            if (shift):
                col.laste_entry=shift.he
                col.in_post_time=get_inpost_t(col)
            else:
                col.laste_entry=None
                col.in_post_time=None
    
        colaborators_all_nbr = collaborateurs.count()
        print(colaborators_all_nbr)
        colaborators_in_nbr =collaborateurs.filter(iwssad=True).count()
        print(colaborators_in_nbr)
        colaborators_out_nbr = collaborateurs.filter(iwssad=False).count()
        print(colaborators_out_nbr)

        male_collabortors_nbr=collaborateurs.filter(gender='H').count()
        female_collabortors_nbr=collaborateurs.filter(gender='F').count()
        # recapitulatif_présence = [colaborators_in,colaborators_out,colaborators_all]
    else :
        colaborators_all_nbr = 0
        colaborators_in_nbr = 0
        colaborators_out_nbr = 0
        
    
    return render(request, 'dash/dash_man.html', locals())


@manger_required
def mes_collaborateurs(request):
    # Get manager
    manger = Employe.objects.filter(user=request.user).get()
    # Get manager team
    try:
        managed_teams =manger.managed_team.all()
    except:
        print("No teams")
    # if he is the team manager we get all employe of this team except the manager
    try:    
        collaborateurs = get_coleagues(manger,managed_teams)
        print(collaborateurs)
        
        # search function by f_name and l_name  
        # Check if request method is GET
        if request.GET:
            # Get str data from fields nom
            nom = request.GET.get('nom').lower()
            status = request.GET.get('status')
            # Check if not None or ''
            if is_valid(nom):
                # Filter list_emp with lastame
                collaborateurs = collaborateurs.filter(Q(user__last_name__istartswith=nom) | Q(
                    user__first_name__istartswith=nom))
            if is_valid(status):
                if status == '1':
                    collaborateurs = collaborateurs.filter(iwssad=True)
                else:
                    collaborateurs = collaborateurs.filter(iwssad=False)
        return render(request, 'dash/mes_collaborateurs.html', {'employes': collaborateurs, 'team': True})
    except:
        print('except')
        return render(request, 'dash/mes_collaborateurs.html', {'team': False})


@manger_required
def fiche_pointage(request):
    # Get manager
    manger = Employe.objects.filter(user=request.user).get()
    # Get managed teams
    managed_teams =manger.managed_team.all()
    try:
        collaborateurs = get_coleagues(manger,managed_teams)
    except:
        print("No team")
    # if he is the team manager we get all employe of this team except the manager
    try:
        
        #managed_teams = Employe.manager.get_my_employe(team, request.user)
        for emp in collaborateurs:
            shifts = emp.get_last_shift()
            if shifts:
                emp.he = shifts.he
                emp.hs = shifts.hs
            else:
                emp.he = None
                emp.hs = None
        # Check if request method is GET
        if request.GET:
            # Get str data from fields nom
            nom = request.GET.get('nom').lower()
            status = request.GET.get('status')
            # Check if not None or ''
            if is_valid(nom):
                # Filter list_emp with lastame
                collaborateurs = collaborateurs.filter(Q(user__last_name__istartswith=nom) | Q(
                    user__first_name__istartswith=nom))
            if is_valid(status):
                if status == '1':
                    collaborateurs = collaborateurs.filter(iwssad=True)
                else:
                    emp.he = None
                    emp.hs = None
    except:
        list_emp = None

    return render(request, 'dash/fiche_pointage.html', {'shifts': collaborateurs})

@manger_required
def mes_equipes(request):
    # Get employe with id
    man = Employe.objects.filter(user=request.user).get()
    teams = Team.objects.filter(manager=man)
    teams_nbr = teams.count()
    if(teams_nbr == 1):
        team=teams.get()
        print(team)
        return HttpResponseRedirect(reverse('dash:equipe_view', kwargs= {'pk':team.id,}))
    
        

    return render(request, 'dash/mes_equipes.html', locals())

@manger_required
def equipe_view(request,pk):
    # Get employe with id
    man = Employe.objects.filter(user=request.user).get()
    team = Team.objects.get(id=pk)
    print(team)
    try:
        coleagues = get_coleagues(man)
    
        if(coleagues):
            for co in coleagues:
                print(co)
    except:
        print("error")
    # the team dashbored part
    # get the team manged by the actuel employe
    try :
        team = Team.objects.filter(manager=man).get()
        print(team)
    # get the employes of the team
    except :
        pass
    if(team):
        colaborators=get_employes(team)
        colaborators_all_nbr = colaborators.count()
        print(colaborators_all_nbr)
        colaborators_in_nbr = get_employes_by_presence(team, True).count()
        print(colaborators_in_nbr)
        colaborators_out_nbr = get_employes_by_presence(team, False).count()
        print(colaborators_out_nbr)

        male_collabortors_nbr=colaborators.filter(gender='H').count()
        female_collabortors_nbr=colaborators.filter(gender='F').count()
        # recapitulatif_présence = [colaborators_in,colaborators_out,colaborators_all]

    else:
        colaborators_all_nbr = 0
        colaborators_in_nbr = 0
        colaborators_out_nbr = 0

    # get colabotators
    if(colaborators):
        for col in colaborators:
            shift=col.get_last_shift()
            if (shift):
                col.laste_entry=shift.he
                col.in_post_time=get_inpost_t(col)
            else:
                col.laste_entry=None
                col.in_post_time=None

    # for c in col :
    #     shift=c.get_last_shift()
    #     entryes=entryes.append(get_laste_entry(shift))
    #     print(entryes)


    return render(request, 'dash/equipe_view.html', locals())
