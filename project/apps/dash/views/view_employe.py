from django.shortcuts import render, HttpResponseRedirect
from apps.dash.decorators import employe_required, manger_required, responsible_required
from django.contrib.auth.decorators import login_required
from apps.pointage.models import Employe, User, Planing, Shift
from django.core.exceptions import ObjectDoesNotExist
from apps.dash.forms import UserForm, EmployeForm, EditUserForm, EditEmployeForm
from django.urls import reverse
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied
from django.utils import timezone
import datetime
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.contrib import messages



# Create your views here.
# get now time
def get_now_t():
    return timezone.localtime(timezone.now()).time()
# to convert naif datetime to number of hours and min


def convert_time(time):
    try:
        days, seconds = time.days, time.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        return "%sh%smin" % (hours, minutes)
    except:
        return "H:M"


def is_valid(param):
    if param != None and param != '':
        return True


def hours_dif(start_t, end_t):
    if (start_t) and (end_t):
        date = datetime.date(1, 1, 1)
        s_t = datetime.datetime.combine(date, start_t)
        e_t = datetime.datetime.combine(date, end_t)
        work_t = e_t-s_t
        # convert the resault in to hours and minuts
        # work_t = convert_time(work_t)
        return work_t
    else:
        return None


def get_laste_entry(shift):
    if (shift):
        print(f'last entry {shift.he}')
        return shift.he

    else:
        print('else of get_last_entry')
        return None


def get_inpost_t(employe):

    shift = employe.get_last_shift()
    he = get_laste_entry(shift)
    now = get_now_t()
    return convert_time(hours_dif(he, now))


def get_time_left(employe):
    try:
        day = employe.get_today_hours()
    except:
        print('day = None')
        return None
    if(day.he1)and (day.hs1):
        if (day.he1 < get_now_t())and (get_now_t() < day.hs1):
            return convert_time(hours_dif(get_now_t(), day.hs1))
        else:
            if(day.he2)and (day.hs2):
                if (day.he2 < get_now_t())and (get_now_t() < day.hs2):
                    return convert_time(hours_dif(get_now_t(), day.hs2))


def get_coleagues(employe):
    if(employe.team):
        team = employe.team
        coleagues = Employe.objects.filter(team=team).exclude(id=employe.id)
        return coleagues

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

@employe_required
def dash_emp(request):

    # Get employe with id
    emp = Employe.objects.filter(user=request.user).get()
    shift = emp.get_last_shift()
    he = get_laste_entry(shift)
    now = get_now_t()
    in_post_t = get_inpost_t(emp)
    try:
        time_left = get_time_left(emp)
    except:
        time_left = "H:M"
    try:
        t_h = emp.get_today_hours()
        todays_hours = [t_h.he1, t_h.hs1, t_h.he2, th.h_s2, ]
    except:
        todays_hours = ['H:M', 'H:M', 'H:M', 'H:M']
    coleagues = get_coleagues(emp)
    if(coleagues):
        for co in coleagues:
            print(co)

    
        # return template with context after convert work_time to hours and min
    return render(request, 'dash/dash_emp.html', {'in_post_t': in_post_t, 'time_left': time_left, 'shift': shift, 'todays_hours': todays_hours, 'coleagues': coleagues})


@login_required
def profile(request):
    # Get the user
    user = request.user
    # Prepopulate UserForm with data
    user_form = UserForm(instance=user)
    # Create grouped form User/Employe
    EmployeFormset = inlineformset_factory(User, Employe, fields=(
        'birthdate', 'birthplace', 'address', 'phone1', 'phone2', 'observation', 'picture', 'gender',), can_delete=False)
    # Prepopulate EmployeForm with user pk
    formset = EmployeFormset(instance=user)

    if request.user.id == user.id:
        if request.method == "POST":
            # get data from POST method
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = EmployeFormset(
                request.POST, request.FILES, instance=user)
            formset.picture = request.FILES.get('picture')
            # If user_form is valide save data
            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = EmployeFormset(
                    request.POST, request.FILES, instance=created_user)
                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect(reverse('dash:profile'))

        return render(request, "dash/profile.html", {
            "user_form": user_form,
            "formset": formset,

        })


@login_required
def view_profile(request, pk):
    # Get the user
    user = User.objects.get(id=pk)
    emp = Employe.objects.filter(user=user).get()
    try:
        planing_pk=emp.planing.id
    except :
        planing_pk=-1    
    # Prepopulate UserForm with data
    user_form = UserForm(instance=user)
    # Create grouped form User/Employe
    EmployeFormset = inlineformset_factory(User, Employe, form=EmployeForm, can_delete=False)
    # Prepopulate EmployeForm with user pk
    formset = EmployeFormset(instance=user)
    
    
    if request.user.id == user.id or request.user.role == 3 or request.user.role == 2:

        if request.method == "POST":
            # get data from POST method
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = EmployeFormset(
                request.POST, request.FILES, instance=user)
            # If user_form is valide save data
            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = EmployeFormset(
                    request.POST, request.FILES, instance=created_user)
                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    messages.success(request, 'Votre observation a était enregistrer')
                    
        return render(request, "dash/profile.html", {
                "user_form": user_form,
                "formset": formset,
                "picture": emp.picture,
                "check": True,
                "planing_pk":planing_pk,
            })

    else:
        return HttpResponseRedirect(reverse('authentification:logout'))

@login_required
def edit_profile(request, pk):
    # Get the user
    user = User.objects.get(id=pk)
    emp = Employe.objects.filter(user=user).get()  
    # Prepopulate UserForm with data
    user_form = EditUserForm(instance=user)
    # Create grouped form User/Employe
    EmployeFormset = inlineformset_factory(User, Employe, form=EditEmployeForm, can_delete=False)
    # Prepopulate EmployeForm with user pk
    formset = EmployeFormset(instance=user)
    
    
    if request.user.id == user.id or request.user.role == 3:

        if request.method == "POST":
            # get data from POST method
            user_form = EditUserForm(request.POST, request.FILES, instance=user)
            formset = EmployeFormset(
                request.POST, request.FILES, instance=user)
            # If user_form is valide save data
            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = EmployeFormset(
                    request.POST, request.FILES, instance=created_user)
                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    
                    return HttpResponseRedirect(reverse('dash:view_profile', kwargs={'pk': pk}))

        return render(request, "dash/edit_profile.html", {
                "user_form": user_form,
                "formset": formset,
                "picture": emp.picture,
                "check": False,
            })

    else:
        return HttpResponseRedirect(reverse('authentification:logout'))

@login_required
def ma_fiche_pointage(request, pk):
    user_asked = User.objects.get(id=pk)
    user_asker = Employe.objects.filter(user=request.user).get()
    emp = Employe.objects.filter(user=user_asked).get()
    # Get the manager of the user_asked
    try:
        manager = emp.team.manager.id
    except:
        manager = None
        print("Le user n'a aucune team")
    if request.user.id == user_asked.id or request.user.role == 3 or user_asker.id == manager:
        # Get shifts of the current employe
        first_shifts = Shift.objects.filter(employe=emp, number=1).values_list(
            'day', 'number', 'he', 'hs').order_by('-day', 'number')
        other_shifts = Shift.objects.exclude(number=1).filter(employe=emp).values_list(
            'day', 'number', 'he', 'hs').order_by('-day', 'number')
        # Check if request method is GET
        if request.GET:
            # Get str data from fields start and end
            start = request.GET.get('start')
            end = request.GET.get('end')
            nbr = request.GET.get('nbr')
            print(nbr)
            # Check if not None or ''
            if is_valid(start) and is_valid(end):
                # Convert str to datetime
                start = datetime.datetime.strptime(start, "%d/%m/%Y")
                end = datetime.datetime.strptime(end, "%d/%m/%Y")
                # Filter shift_list with date params
                first_shifts = first_shifts.filter(Q(day__gte=start), Q(day__lte=end))
            if is_valid(nbr)   :
                if (nbr == '1') :
                    print("in par semaine")
                    days =get_previous_days(7)
                    first_shifts =first_shifts.filter(day__in =days)
                    print(first_shifts)

                if (nbr == '2') :
                    print("in par mois")
                    days =get_previous_days(30)
                    first_shifts =first_shifts.filter(day__in =days)
                    print(first_shifts)    
        # Pagginite my list by 7
        paginator = Paginator(first_shifts, 20)

        # Get id of page from link if empty --> default=1
        page = request.GET.get('page', 1)
        # Get list shift with page number with exceptions if not integer get first page/ if page contains no results get the last page
        try:
            shifts = paginator.page(page)
        except PageNotAnInteger:
            shifts = paginator.page(1)
        except EmptyPage:
            shifts = paginator.page(paginator.num_pages)

        return render(request, 'dash/ma_fiche_pointage.html', {'other_shifts': other_shifts, 'first_shifts': shifts})
    else:
        return render(request, 'dash/ma_fiche_pointage.html', {'other_shifts': None, 'row': None})

@login_required
def my_schedule(request,pk):
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

 
    return render(request, 'dash/responsable/my_schedule.html',{'row':row, 'schedule':schedule, 'pk':pk })

def get_previous_days(n):
    print("from get last week")
    today = timezone.now().date()
    print(today)
    r = range(n)
    last_days=[]
    for i in r :
       last_days.append( today - datetime.timedelta(days=i))
       print (last_days[i])
    
    return last_days


