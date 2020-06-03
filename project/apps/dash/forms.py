from django.forms import ModelForm
from django import forms
from apps.pointage.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ]
    