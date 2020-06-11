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

from django.db.models import Q, Count


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

    if (day.he1 < get_now_t())and (get_now_t() < day.hs1):
        return convert_time(hours_dif(get_now_t(), day.hs1))
    else:
        if (day.he2 < get_now_t())and (get_now_t() < day.hs2):
            return convert_time(hours_dif(get_now_t(), day.hs2))


def get_coleagues(employe):
    if(employe.team):
        team = employe.team
        coleagues = Employe.objects.filter(team=team).exclude(id=employe.id)
        return coleagues


@employe_required
def dash_emp(request):
    # Get employe with id
    emp = Employe.objects.filter(user=request.user).get()
    shift = emp.get_last_shift()
    he = get_laste_entry(shift)
    now = get_now_t()
    in_post_t = get_inpost_t(emp)
    time_left = get_time_left(emp)
    try:
        th = emp.get_today_hours()
        todays_hours = [th.he1, th.hs1, th.he2, th.hs2, ]
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
        'birthdate', 'birthplace', 'address', 'phone1', 'phone2', 'observation', 'picture', 'gender'), can_delete=False)
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
    check = 1
    user = User.objects.get(id=pk)
    emp = Employe.objects.filter(user=user).get()
    # Prepopulate UserForm with data
    user_form = UserForm(instance=user)
    # Create grouped form User/Employe
    EmployeFormset = inlineformset_factory(User, Employe, fields=(
        'birthdate', 'birthplace', 'address', 'phone1', 'phone2', 'observation', 'picture', 'gender'), can_delete=False)
    # Prepopulate EmployeForm with user pk
    formset = EmployeFormset(instance=user)

    if request.user.id == user.id or request.user.role == 3 or request.user.role == 2:
        
        if request.user.role == 2:
            if str(request.user.pk) != str(pk):  
                check = 2

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
                    return HttpResponseRedirect(reverse('dash:view_profile', kwargs={'pk': pk}))

        if request.GET.get('edit_profile') != None:
            return render(request, "dash/profile.html", {
                "user_form": user_form,
                "formset": formset,
                "picture": emp.picture,
                "check": False,
            })
        else:
            return render(request, "dash/profile.html", {
                "user_form": user_form,
                "formset": formset,
                "picture": emp.picture,
                "check": check,
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
            # Check if not None or ''
            if is_valid(start) and is_valid(end):
                # Convert str to datetime
                start = datetime.datetime.strptime(start, "%d/%m/%Y")
                end = datetime.datetime.strptime(end, "%d/%m/%Y")
                # Filter shift_list with date params
                first_shifts = first_shifts.filter(Q(day__gte=start), Q(day__lte=end))
        # Pagginite my list by 7
        paginator = Paginator(first_shifts, 7)

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



