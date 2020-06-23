from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from apps.dash.decorators import employe_required, manger_required, responsible_required
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
from apps.dash.views import get_now_t, convert_time, is_valid, hours_dif, get_laste_entry, get_inpost_t, get_time_left,get_now_t,get_employes,get_employes_by_presence


from django.db.models import Count
from django.forms import inlineformset_factory
from apps.pointage.resources import ShiftResource
from tablib import Dataset

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




@responsible_required
def dash_responsible(request):
    # get the responsible
    responsible=Employe.objects.filter(user=request.user).get()
    # get responsible dash parts
    shift = responsible.get_last_shift()
    he = get_laste_entry(shift)
    now = get_now_t()
    in_post_t = get_inpost_t(responsible)
    time_left = get_time_left(responsible)
    try:
        t_h = responsible.get_today_hours()
        todays_hours = [t_h.he1, t_h.hs1, t_h.he2, t_h.hs2, ]
    except:
        todays_hours = ['H:M', 'H:M', 'H:M', 'H:M']

    # get teams
    teams = Team.objects.all()
    teams_nbr = teams.count()
    # get all the managers 
    managers = Employe.objects.filter(~Q(managed_team=None))
    # print(managers)
    managers_nbr=managers.count()
    managers_in_nbr=managers.filter(iwssad=True).count()
    managers_out_nbr=managers.filter(iwssad=False).count()
    # print(f'les manager présents {managers_in}')
    # print(f'les manager sortie {managers_out}')
    # get the number of employes by team
    if (teams):
        for team in teams :
            team.nbr_members=get_employes(team).count()
            team.nbr_in= get_employes_by_presence(team,True).count()
            team.nbr_out= get_employes_by_presence(team,False).count()
            #print(team.nbr_members)

    # les collaborateurs 
    collaborateurs=Employe.objects.all()
    collaborateurs_nbr=collaborateurs.count()
    print(collaborateurs)
    print(collaborateurs_nbr)
    male_collaborateurs_nbr=collaborateurs.filter(gender='H').count()
    female_collaborateurs_nbr=collaborateurs.filter(gender='F').count()
    collaborateurs_in_nbr=collaborateurs.filter(iwssad=True).count()
    collaborateurs_out_nbr=collaborateurs.filter(iwssad=False).count()
    # add last_entry and in poste time to employes queryset
    if(collaborateurs):
        for col in collaborateurs :
            shift=col.get_last_shift()
            print(shift)
            col.last_entry=get_laste_entry(shift)
            print(col.last_entry)
            col.in_post_t = get_inpost_t(col)
            print( col.in_post_t)
    
    
    return render(request, 'dash/responsable/dash_responsible.html',locals())

@responsible_required
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


@responsible_required
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


@responsible_required
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
            return HttpResponseRedirect(reverse('dash:assign_schedule', kwargs={'pk': planning.id}))
    else:
        form = PlanningForm()
        formset = DayFormSet(initial=initial)


    return render(request, 'dash/responsable/create_schedule.html', {'form': form, 'formset': formset})

@responsible_required
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
            return HttpResponseRedirect(reverse('dash:assign_team', kwargs={'pk': team.id}))
    else:
        form = TeamForm()

    return render(request, 'dash/create_team.html', {'form': form})

@responsible_required
def assign_team(request, pk):
    
    if 'term' in request.GET: 
        term = request.GET.get('term')
        employes = Employe.objects.filter(Q(team=None), (Q(user__last_name__istartswith=term) | Q(user__first_name__istartswith=term)))
        employes_list = list()
        print(employes)
        for employe in employes:
            employes_list.append(employe.user.last_name+' '+employe.user.first_name)

        return JsonResponse(employes_list, safe=False)

    team = Team.objects.filter(id=pk).get()
    employes = Employe.objects.filter(team=team)

    form = TeamForm(instance=team)
    form.fields['manager'].widget.attrs['disabled'] = 'disabled'
    form.fields['titre'].widget.attrs['readonly'] = True
    form.fields['description'].widget.attrs['readonly'] = True

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

    return render(request, 'dash/assign_team.html', {'form': form, 'employes':employes, 'pk':pk})

@responsible_required
def modify_team(request, pk):
    # Get team
    team = Team.objects.filter(id=pk).get()
    
    if request.POST:
        form = TeamForm(request.POST, instance=team)
        if form.is_valid():
            form.save()
            print('saving team')  
            form = TeamForm(instance=team) 
            return HttpResponseRedirect(reverse('dash:assign_team', kwargs={'pk': pk}))
    else:
        form = TeamForm(instance=team)

    return render(request, 'dash/responsable/modify_team.html', {'form': form})


@responsible_required
def assign_schedule(request, pk):

    if 'term' in request.GET:
        term = request.GET.get('term')
        employes = Employe.objects.filter(Q(user__last_name__istartswith=term) | Q(user__first_name__istartswith=term))
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
@responsible_required
def delete_employe_team(request, pk):
    # Get employe with the pk in url
    print('id',pk)
    user = User.objects.get(id=pk)
    employe = Employe.objects.filter(user=user).get()
    # Get team id for redirect to the modification interface after delete employe
    pk = employe.team.id
    # Delete employe from team
    employe.team = None
    employe.save()
    # Redirect with reverse 
    return HttpResponseRedirect(reverse('dash:assign_team', kwargs={'pk': pk}))

@responsible_required
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

@responsible_required
def delete_schedule(request, pk):
    try:
        schedule = Planing.objects.get(id=pk).delete()
    except:
        print("None schedule to delete")
    return HttpResponseRedirect(reverse('dash:schedules'))

@responsible_required
def delete_team(request, pk):
    try:
        team = Team.objects.get(id=pk).delete()
    except:
        print("None team to delete")
    return HttpResponseRedirect(reverse('dash:my_teams'))


    


@responsible_required
def mes_employes(request):
    # Get responsable
    responsable = Employe.objects.filter(user=request.user).get()
    # Exclude from list
    list_emp = Employe.objects.exclude(id=responsable.id)
        # Check if request method is GET
    if request.GET:
        # Get str data from fields nom
        nom = request.GET.get('nom')
        status = request.GET.get('status')
        # Check if not None or ''
        if is_valid(nom):
            # Filter list_emp with lastame
            list_emp = list_emp.filter(Q(user__last_name__istartswith=nom) | Q(user__first_name__istartswith=nom))
                    
        if is_valid(status):
            if status == '1':
                list_emp = list_emp.filter(iwssad=True)
            else:
                list_emp = list_emp.filter(iwssad=False)

    return render(request, 'dash/mes_collaborateurs.html', {'employes':list_emp})

@responsible_required
def fiche_pointage_all(request):
    # Get responsable
    responsable = Employe.objects.filter(user=request.user).get()
    # Exclude from list
    list_emp = Employe.objects.exclude(id=responsable.id)
    # if he is the team manager we get all employe of this team except the manager 
    for emp in list_emp:
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
        nom = request.GET.get('nom')
        status = request.GET.get('status')
        # Check if not None or ''
        if is_valid(nom):
            # Filter list_emp with lastame
            list_emp = list_emp.filter(Q(user__last_name__istartswith=nom) | Q(user__first_name__istartswith=nom))
        if is_valid(status):
            if status == '1':
                list_emp = list_emp.filter(iwssad=True)
            else:
                emp.he = None
                emp.hs = None
                
                
    return render(request, 'dash/fiche_pointage.html',{'shifts':list_emp})


def export_shift(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        shift_resource = ShiftResource()
        dataset = shift_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response        
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
            return response   

def import_shift(request):
    if request.method == 'POST':
        shift_resource = ShiftResource()
        dataset = Dataset()
        shifts = request.FILES['ShiftData']

        imported_data = dataset.load(shifts.read())
        result = shift_resource.import_data(dataset, dry_run=True)  

        if not result.has_errors():
            # Import now
            shift_resource.import_data(dataset, dry_run=False)
    
    return HttpResponseRedirect(reverse('dash:fiche_pointage_all'))


