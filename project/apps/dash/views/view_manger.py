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
    todays_hours = emp.get_today_hours()
    coleagues = get_coleagues(emp)
    for co in coleagues:
        print(co)
    # return template with context after convert work_time to hours and min
    return render(request, 'dash/dash_man.html', {'in_post_t': in_post_t, 'time_left': time_left, 'shift': shift, 'todays_hours': todays_hours, 'coleagues': coleagues})