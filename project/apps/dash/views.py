from django.shortcuts import render
from .decorators import employe_required, manger_required, project_manger_required

# Create your views here.


@employe_required
def dash_emp(request):
    return render(request, 'dash/dash_emp.html')


@manger_required
def dash_man(request):
    return render(request, 'dash/dash_man.html')


@project_manger_required
def dash_pro_man(request):
    return render(request, 'dash/dash_pro_man.html')
