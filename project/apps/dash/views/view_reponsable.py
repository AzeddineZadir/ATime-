from django.shortcuts import render, HttpResponseRedirect
from apps.dash.decorators import employe_required, manger_required, project_manger_required
from django.contrib.auth.decorators import login_required
from apps.pointage.models import Employe, User, Planing, Shift, Team, Day
from django.core.exceptions import ObjectDoesNotExist
from apps.dash.forms import UserForm, TeamForm, DayForm, PlanningForm
from django.urls import reverse
from django.forms.models import inlineformset_factory, modelformset_factory
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
def schedule(request, pk):
    schedule = Planing.objects.filter(id=pk).annotate(nb_emp=Count('pemployes')).get()

    total = datetime.timedelta(hours=0)
    for day in schedule.planing_days.all():     
        total += sum_hours_planning_day(day)
    schedule.total = convert_time(total)

         
    row = dict()
    for day in schedule.planing_days.all():
        date = datetime.date(1, 1, 1)
        dateE = datetime.datetime(1, 1, 1, 0, 0)
        dateS = datetime.datetime(1, 1, 2, 0, 0)
        try:
            he1 = datetime.datetime.combine(date, day.he1)
            hs1 = datetime.datetime.combine(date, day.hs1)
        except:
            he1 = dateE
            hs1 = dateE

        try:
            he2 = datetime.datetime.combine(date, day.he2)
            hs2 = datetime.datetime.combine(date, day.hs2)           
        except:
            he2 = dateS
            hs2 = dateS
        row[day] = {'title':'', 'he1':he1, 'hs1':hs1, 'he2':he2, 'hs2':hs2, 'jours':day.get_jds_display()}

 
    return render(request, 'dash/responsable/schedule.html',{'row':row, 'schedule':schedule, 'pk':pk })

@project_manger_required
def create_schedule(request):
    DayFormSet = inlineformset_factory(Planing, Day, form=DayForm, extra=7,max_num=7 ,can_delete=False)
    #some_formset = DayFormSet(initial=[{'jds': 6}, {'jds': 0}, {'jds': 1}, {'jds': 2}, {'jds': 3}, {'jds': 4}, {'jds': 5}])
    initial=[{'jds': 6}, {'jds': 0}, {'jds': 1}, {'jds': 2}, {'jds': 3}, {'jds': 4}, {'jds': 5}]

    if request.method == 'POST':
        form = PlanningForm(request.POST)
        formset = DayFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            planning = form.save()
            instances = formset.save(commit=False)
            for instance in instances:
                print(instance.jds)
                instance.planing = planning
                instance.save()
            print('saving planning')
    else:
        form = PlanningForm()
        formset = DayFormSet(initial=initial)


    return render(request, 'dash/responsable/create_schedule.html', {'form': form, 'formset': formset})

@project_manger_required
def modify_schedule(request, pk):
    initial=[{'jds': 6}, {'jds': 0}, {'jds': 1}, {'jds': 2}, {'jds': 3}, {'jds': 4}, {'jds': 5}]
    schedule = Planing.objects.get(pk=pk)
    DayFormSet = inlineformset_factory(Planing, Day, form=DayForm,extra=7,max_num=7)

    if request.method == "POST":
        planning_form = PlanningForm(request.POST, request.FILES, instance=schedule)
        formset = DayFormSet(request.POST, request.FILES, instance=schedule)
        if planning_form.is_valid(): 
            created_schedule = planning_form.save()
            formset = DayFormSet(request.POST, instance=created_schedule)   
            if formset.is_valid():
                formset.save()
            return HttpResponseRedirect(reverse('dash:schedule', kwargs={'pk': pk}))
    else:
        planning_form = PlanningForm(instance=schedule)
        formset = DayFormSet(instance=schedule)

    return render(request, 'dash/responsable/modify_schedule.html',{'form':planning_form, 'formset':formset })

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

def assign_schedule(request, pk):

    if 'term' in request.GET: 
        employes = Employe.objects.filter(team=None, user__last_name__istartswith=request.GET.get('term'))
        employes_list = list()
        for employe in employes:
            employes_list.append(employe.user.last_name+' '+employe.user.first_name)
        return JsonResponse(employes_list, safe=False)

    schedule = Planing.objects.filter(id=pk).get()
    employes = Employe.objects.filter(planing=schedule)

    if 'add' in request.POST:
        employe = request.POST.get('employe')
        employe=employe.split(" ", 1)
        if len(employe) > 1:
            try:
                employe = Employe.objects.filter(user__last_name=employe[0], user__first_name=employe[1]).get()
                if employe.planing == None:
                    employe.planing = schedule
                    employe.save()           
            except ObjectDoesNotExist:
                print("Employe does not exist") 

    return render(request, 'dash/responsable/assign_schedule.html', {'pk':pk, 'employes':employes})


# View to delete employe from team
@project_manger_required
def delete_employe_team(request, pk):
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

@project_manger_required
def delete_employe_schedule(request, pk):
    # Get employe with the pk in url
    user = User.objects.get(id=pk)
    employe = Employe.objects.filter(user=user).get()
    # Get team id for redirect to the modification interface after delete employe
    pk = employe.planing.id
    # Delete employe from team
    employe.planing = None
    employe.save()
    # Redirect with reverse 
    return HttpResponseRedirect(reverse('dash:assign_schedule', kwargs={'pk': pk}))

