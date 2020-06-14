from django.shortcuts import render, HttpResponseRedirect
from apps.dash.decorators import employe_required, manger_required, project_manger_required
from django.contrib.auth.decorators import login_required
from apps.pointage.models import Employe, User, Planing, Shift, Team
from django.core.exceptions import ObjectDoesNotExist
from apps.dash.forms import UserForm, TeamForm, DayForm
from django.urls import reverse
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.utils import timezone
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.http import JsonResponse


@project_manger_required
def dash_pro_man(request):
    return render(request, 'dash/dash_pro_man.html', {'test': 4})

@project_manger_required
def my_teams(request):
    
    return render(request, 'dash/responsable/my_teams.html')


def create_team(request):
    #managers = Employe.objects.filter(user__role=2, managed_team=None)

    if 'term' in request.GET: 
        employes = Employe.objects.filter(team=None, user__last_name__istartswith=request.GET.get('term'))
        employes_list = list()
        print(employes)
        for employe in employes:
            employes_list.append(employe.user.last_name+' '+employe.user.first_name)

        return JsonResponse(employes_list, safe=False)

    if 'test' in request.POST:
        s = request.POST.get('test')
        s=s.split(" ", 1)
        employe = Employe.objects.filter(user__last_name=s[0], user__first_name=s[1]).get()
        team = Team.objects.filter(titre='test3').get()
        print(team)
        employe.team=team
        employe.save()
        print(employe)

    if 'create' in request.POST:
        print('create POST')
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            print('saving team')
            return HttpResponseRedirect(reverse('dash:modify_team', kwargs={'titre': team.titre}))
    else:
        form = TeamForm()

    return render(request, 'dash/create_team.html', {'form': form})

def modify_team(request, pk):
    
    if 'term' in request.GET: 
        employes = Employe.objects.filter(team=None, user__last_name__istartswith=request.GET.get('term'))
        employes_list = list()
        print(employes)
        for employe in employes:
            employes_list.append(employe.user.last_name+' '+employe.user.first_name)

        return JsonResponse(employes_list, safe=False)

    team = Team.objects.filter(id=pk).get()
    employes = Employe.objects.filter(team=team)
    
    if 'modify' in request.POST:
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            print('saving team')  
            form = TeamForm(instance=team) 
    else:
        form = TeamForm(instance=team)

    if 'add' in request.POST:
        employe = request.POST.get('employe')
        print(employe)
        employe=employe.split(" ", 1)
        if len(employe) > 1:
            try:
                employe = Employe.objects.filter(user__last_name=employe[0], user__first_name=employe[1]).get()
                if employe.team == None:
                    employe.team = team
                    employe.save()           
            except ObjectDoesNotExist:
                print("Employe does not exist")  

    return render(request, 'dash/modify_team.html', {'form': form, 'employes':employes})

def create_schedule(request):
    #managers = Employe.objects.filter(user__role=2, managed_team=None)

    if request.method == 'POST':
        form = DayForm(request.POST)
        if form.is_valid():
            team = form.save()
            print('saving team')
    else:
        form = DayForm()

    return render(request, 'dash/create_schedule.html', {'form': form})

# View to delete employe from team
@project_manger_required
def view_delete_employe_team(request, pk):
    # Get employe with the pk in url
    user = User.objects.get(id=pk)
    employe = Employe.objects.filter(user=user).get()
    # Get team id for redirect to the modification interface after delete employe
    pk = employe.team.id
    # Delete employe from team
    employe.team = None
    employe.save()
    # Redirect with reverse 
    return HttpResponseRedirect(reverse('dash:modify_team', kwargs={'pk': pk}))

