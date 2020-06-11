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

# get now time
def get_now_t():
    return timezone.localtime(timezone.now()).time()
# to convert naif datetime to number of hours and min

def is_valid(param):
    if param != None and param != '':
        return True

def get_coleagues(employe):
    if(employe.team):
        team = employe.team
        coleagues = Employe.objects.filter(team=team).exclude(id=employe.id)
        return coleagues

def get_laste_entry(shift):
    if (shift):
        print(f'last entry {shift.he}')
        return shift.he
    else:
        print('else of get_last_entry')
        return None

def convert_time(time):
    try:
        days, seconds = time.days, time.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        return "%sh%smin" % (hours, minutes)
    except:
        return "h:m"

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

@manger_required
def dash_man(request):
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
    return render(request, 'dash/dash_man.html', {'in_post_t': in_post_t, 'time_left': time_left, 'shift': shift, 'todays_hours': todays_hours, 'coleagues': coleagues})


@manger_required
def mes_collaborateurs(request):
    # Get manager
    manger = Employe.objects.filter(user=request.user).get()
    # Get manager team
    team = manger.team
    # if he is the team manager we get all employe of this team except the manager  
    if manger == team.manager:
        list_emp = Employe.manager.get_my_employe(team,request.user)
         # Check if request method is GET
        if request.GET:
            # Get str data from fields nom
            nom = request.GET.get('nom').lower()
            status = request.GET.get('status')
            # Check if not None or ''
            if is_valid(nom):
                # Filter list_emp with lastame
                list_emp = list_emp.filter(user__last_name=nom)
                
            if is_valid(status):
                if status == '1':
                    list_emp = list_emp.filter(iwssad=True)
                else:
                    list_emp = list_emp.filter(iwssad=False)

        return render(request, 'dash/mes_collaborateurs.html', {'employes':list_emp, 'team':True})
    else:
        return render(request, 'dash/mes_collaborateurs.html',{'team':False})


@manger_required   
def fiche_pointage(request):
    # Get manager
    manger = Employe.objects.filter(user=request.user).get()
    # Get manager team
    team = manger.team
    # if he is the team manager we get all employe of this team except the manager  
    if manger == team.manager:
        list_emp = Employe.manager.get_my_employe(team,request.user)
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
            nom = request.GET.get('nom').lower()
            status = request.GET.get('status')
        
            print(status)
            # Check if not None or ''
            if is_valid(nom):
                # Filter list_emp with lastame
                list_emp = list_emp.filter(user__last_name=nom)
            if is_valid(status):
                if status == '1':
                    list_emp = list_emp.filter(iwssad=True)
                else:
                    list_emp = list_emp.filter(iwssad=False)

                
                
    return render(request, 'dash/fiche_pointage.html',{'shifts':list_emp})

   
    

    
