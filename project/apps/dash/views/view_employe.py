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


# Create your views here.

# to convert naif datetime to number of hours and min
def convert_time(time):
    days, seconds = time.days, time.seconds
    hours = days * 24 + seconds // 3600
    minutes = (seconds % 3600) // 60
    return "%sh%smin" % (hours, minutes)


def is_valid(param):
    if param != None and param != '':
        return True


@employe_required
def dash_emp(request):
    # Get employe with id
    emp = Employe.objects.filter(user=request.user).get()
    # Get date time when the employe begin work
    time = emp.get_start_time()
    # start time - time now
    print("-----", time)
    print("-----", timezone.now().time())
    date = datetime.date(1, 1, 1)
    if (time):
        datetime1 = datetime.datetime.combine(date, timezone.now().time())
        datetime2 = datetime.datetime.combine(date, time)
        work_time = datetime1-datetime2
        work_time = convert_time(work_time)
    else:
        work_time = None
    # return template with context after convert work_time to hours and min
    return render(request, 'dash/dash_emp.html', {'time': time, 'work_time': work_time})


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
    user = User.objects.get(id=pk)
    # Prepopulate UserForm with data
    user_form = UserForm(instance=user)
    # Create grouped form User/Employe
    EmployeFormset = inlineformset_factory(User, Employe, fields=(
        'birthdate', 'birthplace', 'address', 'phone1', 'phone2', 'observation', 'picture', 'gender'), can_delete=False)
    # Prepopulate EmployeForm with user pk
    formset = EmployeFormset(instance=user)

    if request.user.id == user.id or request.user.role == 3:
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

        if request.GET.get('edit_profile') == pk:
            return render(request, "dash/profile.html", {
                "user_form": user_form,
                "formset": formset,
                "check": False,
            })
        else:
            return render(request, "dash/profile.html", {
                "user_form": user_form,
                "formset": formset,
                "check": pk,
            })

    else:
        return HttpResponseRedirect(reverse('authentification:logout'))


@login_required
def ma_fiche_pointage(request):
    emp = Employe.objects.filter(user=request.user).get()
    # Get shifts of the current employe
    shift_list = Shift.objects.filter(employe=emp).order_by('-day')
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
            shift_list = shift_list.filter(Q(day__gte=start), Q(day__lte=end))
    # Pagginite my list by 7
    paginator = Paginator(shift_list, 7)
    # Get id of page from link if empty --> default=1
    page = request.GET.get('page', 1)
    # Get list shift with page number with exceptions if not integer get first page/ if page contains no results get the last page
    try:
        shifts = paginator.page(page)
    except PageNotAnInteger:
        shifts = paginator.page(1)
    except EmptyPage:
        shifts = paginator.page(paginator.num_pages)
    
    return render(request, 'dash/ma_fiche_pointage.html', {'shifts': shifts})


@manger_required
def mes_collaborateurs(request):
    return render(request, 'dash/mes_collaborateurs.html')


