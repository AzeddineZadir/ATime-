from django.shortcuts import render

# Create your views here.


def dash_emp(request):
    return render(request, 'dash/dash_emp.html')


def dash_man(request):
    return render(request, 'dash/dash_man.html')


def dash_pro_man(request):
    return render(request, 'dash/dash_pro_man.html')
