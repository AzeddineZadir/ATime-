from django.shortcuts import render, HttpResponseRedirect
from apps.dash.decorators import employe_required, manger_required, project_manger_required
from django.contrib.auth.decorators import login_required
from apps.pointage.models import Employe, User, Planing, Shift, Team, Day
from django.core.exceptions import ObjectDoesNotExist
from apps.dash.forms import UserForm, TeamForm, DayForm, PlaningForm
from django.urls import reverse
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.utils import timezone
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from apps.dash.views import hours_dif, convert_time
from django.db.models import Q
from django.http import JsonResponse

from django.db.models import Count
from django.forms import inlineformset_factory

# Return the sum of hours in day
def sum_hours_planning_day(day):
    if day.he1 != None and day.hs1 != None:
        p1=hours_dif(day.he1, day.hs1)
    else:
        p1=datetime.timedelta(hours=0)
    
    if day.he2 != None and day.hs2 != None:
        p2=hours_dif(day.he2, day.hs2)
    else:
        p2=datetime.timedelta(hours=0)

    return p1+p2



@project_manger_required
def dash_pro_man(request):
    return render(request, 'dash/dash_pro_man.html', {'test': 4})

@project_manger_required
def my_teams(request):
    teams = Team.objects.annotate(nb_emp_in=Count(
            'employes',
            filter=Q(employes__iwssad=True)),
            nb_emp=Count(
            'employes'
        ))

    for team in teams:
        print(team.nb_emp_in, team.nb_emp, team.titre) 

    return render(request, 'dash/responsable/my_teams.html', {'teams':teams})


@project_manger_required
def schedules(request):
    # Get list off all schudules 
    schedules = Planing.objects.filter()
    for schedule in schedules:
        total = datetime.timedelta(hours=0)
        for day in schedule.planing_days.all():     
            total += sum_hours_planning_day(day)
        schedule.total = convert_time(total)
        print('Nom du planning', schedule)
        print('Nom du planning', schedule.description)
        print('total', schedule.total)

    return render(request, 'dash/responsable/schedules.html', {'schedules':schedules})

@project_manger_required
def schedule(request):
    planning = Planing.objects.filter(titre='employe').get()
    
    date = datetime.datetime(1, 1, 1,12,0,0)
    date1 = datetime.datetime(1, 1, 1,18,0,0)
   

    innerdict = {}
    emp = {}
    emp = {'d':{'jours': 'samedi', 'date': date, 'date1':date1, 'title':'tt'}}
    res = dict()
    for i in range(3):
        res[i] = {'title':'tt','date1':date1,'date':date,'jours':'samedi'}
 
    return render(request, 'dash/responsable/schedule.html',{'m1':res})

@project_manger_required
def create_schedule(request):
    DayFormSet = inlineformset_factory(Planing, Day, form=DayForm, extra=7, can_delete=False)
    #some_formset = DayFormSet(initial=[{'jds': 6}, {'jds': 0}, {'jds': 1}, {'jds': 2}, {'jds': 3}, {'jds': 4}, {'jds': 5}])
    initial=[{'jds': 6}, {'jds': 0}, {'jds': 1}, {'jds': 2}, {'jds': 3}, {'jds': 4}, {'jds': 5}]

    if request.method == 'POST':
        form = PlaningForm(request.POST)
        formset = DayFormSet(request.POST, initial=initial)
        if form.is_valid() and formset.is_valid():
            planning = form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                print(instance.jds)
                instance.planing = planning
                instance.save()
            print('saving planning')
    else:
        form = PlaningForm()
        formset = DayFormSet(initial=initial)


    return render(request, 'dash/responsable/create_schedule.html', {'form': form, 'formset': formset})


def create_team(request):

    if 'create' in request.POST:
        form = TeamForm(request.POST)
        if form.is_valid():
            team = form.save()
            return HttpResponseRedirect(reverse('dash:modify_team', kwargs={'pk': team.id}))
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

