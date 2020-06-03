from django.shortcuts import render, HttpResponseRedirect
from .decorators import employe_required, manger_required, project_manger_required
from django.contrib.auth.decorators import login_required
from apps.pointage.models import Employe, User
from django.core.exceptions import ObjectDoesNotExist
from .forms import UserForm
from django.urls import reverse
from django.forms.models import inlineformset_factory
from django.core.exceptions import PermissionDenied

# Create your views here.


@employe_required
def dash_emp(request):
    return render(request, 'dash/dash_emp.html')


@manger_required
def dash_man(request):
    # Get current user manager
    emp_man = Employe.objects.filter(user=request.user).get()
    # Get number of employe --> total/inside/outside
    print(emp_man.team)
    if emp_man.team != None:
        print("test")
        man_employe_stats = Employe.manager.get_my_employe_stats(team=emp_man.team, user_emp=request.user).get()
        team_name = emp_man.team.nom
    # Get all employe of current manager
        man_employe = Employe.manager.get_my_employe(team=emp_man.team, user_emp=request.user)
    else:
        man_employe_stats = None
        team_name = None
        man_employe = None

    return render(request, 'dash/dash_man.html', {'man_employe_stats':man_employe_stats, 'team_name':team_name, 'man_employe':man_employe})


@project_manger_required
def dash_pro_man(request):
    return render(request, 'dash/dash_pro_man.html', {'test':4})


def profile(request):
    # Get the user
    user = request.user
    # Prepopulate UserForm with data
    user_form = UserForm(instance=user)
    # Create grouped form User/Employe 
    EmployeFormset = inlineformset_factory(User, Employe, fields=('birthdate', 'birthplace', 'address', 'phone1', 'phone2', 'observation', 'picture'), can_delete=False)
    # Prepopulate EmployeForm with user pk
    formset = EmployeFormset(instance=user)
 
    if request.user.id == user.id:
        if request.method == "POST":
            # get data from POST method
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = EmployeFormset(request.POST, request.FILES, instance=user)
            # If user_form is valide save data
            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = EmployeFormset(request.POST, request.FILES, instance=created_user)
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
    EmployeFormset = inlineformset_factory(User, Employe, fields=('birthdate', 'birthplace', 'address', 'phone1', 'phone2', 'observation', 'picture'), can_delete=False)
    # Prepopulate EmployeForm with user pk
    formset = EmployeFormset(instance=user)
 
    if request.user.id == user.id or request.user.role == 3:
        if request.method == "POST":
            # get data from POST method
            user_form = UserForm(request.POST, request.FILES, instance=user)
            formset = EmployeFormset(request.POST, request.FILES, instance=user)
            # If user_form is valide save data
            if user_form.is_valid():
                created_user = user_form.save(commit=False)
                formset = EmployeFormset(request.POST, request.FILES, instance=created_user)
                if formset.is_valid():
                    created_user.save()
                    formset.save()
                    return HttpResponseRedirect(reverse('dash:view_profile', kwargs={'pk': pk}))
 
        return render(request, "dash/profile.html", {
            "user_form": user_form,
            "formset": formset,
        })

  