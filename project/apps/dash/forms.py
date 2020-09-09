from django.forms import ModelForm, HiddenInput, TimeField, TextInput
from django import forms
from apps.pointage.models import User, Employe, Team, Planing, Day
from django.db.models import Q
from crispy_forms.helper import FormHelper

class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['role'].widget = HiddenInput()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email','role' ]
        help_texts = {
            'username': None,
        }
        widgets = {
        'username': forms.TextInput(attrs={'readonly': 'readonly'}),
        'last_name': forms.TextInput(attrs={'readonly': 'readonly'}),
        'first_name': forms.TextInput(attrs={'readonly': 'readonly'}),
        'email': forms.TextInput(attrs={'readonly': 'readonly'}),
        'role': forms.TextInput(attrs={'readonly': 'readonly'}),
        }

class EditUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
        self.fields['role'].widget = HiddenInput()

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email','role' ]
        widgets = {
        'last_name': forms.TextInput(attrs={'readonly': 'readonly'}),
        'first_name': forms.TextInput(attrs={'readonly': 'readonly'}),
        'role': forms.TextInput(attrs={'readonly': 'readonly'}),
        }
        help_texts = {
            'username': None,
        }
        

class EmployeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EmployeForm, self).__init__(*args, **kwargs)
        self.fields['planing'].widget = HiddenInput()

    class Meta:
        model = Employe
        fields = ['user', 'birthdate', 'birthplace', 'address', 'phone1', 'phone2', 'description', 'gender','planing', 'observation']
        widgets = {
            'user': forms.TextInput(attrs={'readonly': 'readonly'}),
            'birthdate': forms.TextInput(attrs={'readonly': 'readonly'}),
            'birthplace': forms.TextInput(attrs={'readonly': 'readonly'}),
            'address': forms.TextInput(attrs={'readonly': 'readonly'}),
            'phone1': forms.TextInput(attrs={'readonly': 'readonly'}),
            'phone2': forms.TextInput(attrs={'readonly': 'readonly'}),
            'description': forms.Textarea(attrs={'readonly': 'readonly','rows': 3}),
            'gender': forms.TextInput(attrs={'readonly': 'readonly'}),
            'planing': forms.TextInput(attrs={'readonly': 'readonly'}),  
            
            }

class EditEmployeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditEmployeForm, self).__init__(*args, **kwargs)
        self.fields['planing'].widget = HiddenInput()

    class Meta:
        model = Employe
        fields = ['user', 'birthdate', 'birthplace', 'address', 'phone1', 'phone2', 'description', 'picture', 'gender','planing', 'observation']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'picture':forms.FileInput(attrs={'class':'custom-file-input' }) 
        }



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
            try:
                self.fields['manager'].queryset = Employe.objects.filter(Q(user__role=2),( Q(user=team.manager.user) | Q(managed_team=None) ))
                self.fields['manager'].initial = team.manager
            except:
                self.fields['manager'].queryset = Employe.objects.filter(Q(user__role=2), Q(managed_team=None) )
                print("Manager does not exists")

    class Meta:
        model = Team
        fields = ['id', 'titre', 'description', 'manager' ]

class PlanningForm(forms.ModelForm):

    class Meta:
        model = Planing
        fields =    '__all__'

class DayForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(DayForm, self).__init__(*args, **kwargs)
        days = ['Lundi', 'Mardi', 'Mercredi' , 'Jeudi' , 'Vendredi', 'Samedi', 'Dimanche']
        # Hide jds field
        self.fields['jds'].widget = HiddenInput()
        # Get FormHelper to remove all labels
        self.helper = FormHelper()
        self.helper.form_show_labels = False 
        if 'initial' in kwargs:
            t = kwargs.get('initial').get('jds')
            self.day= days[t]
        else:
            print("None")

        if 'instance' in kwargs :
            instance = kwargs.pop('instance')
            self.day=days[instance.jds]
        else:
            team = None
        
        # Adding placeholder to fields
        self.fields['he1'].widget.attrs['placeholder'] = "Heure d'entré"
        self.fields['hs1'].widget.attrs['placeholder'] = "Heure de sortie"
        self.fields['he2'].widget.attrs['placeholder'] = "Heure d'entré"
        self.fields['hs2'].widget.attrs['placeholder'] = "Heure de sortie"
        

    class Meta:
        model = Day
        fields =    '__all__'

   
    