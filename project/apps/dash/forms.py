from django.forms import ModelForm
from django import forms
from apps.pointage.models import User, Employe, Team, Planing
from django.db.models import Q


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ]


class TeamForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):     
        super (TeamForm,self ).__init__(*args,**kwargs) 
        if 'instance' in kwargs :
            team = kwargs.pop('instance')
        else:
            team = None

        if team == None:
            self.fields['manager'].queryset = Employe.objects.filter(user__role=2, managed_team=None)
        else:
            self.fields['manager'].queryset = Employe.objects.filter(Q(user__role=2),( Q(user=team.manager.user) | Q(managed_team=None) ))
            self.fields['manager'].initial = team.manager

    class Meta:
        model = Team
        fields = ['id', 'titre', 'description', 'manager' ]

class DayForm(forms.ModelForm):


    class Meta:
        model = Planing
        fields =    '__all__'

   
    