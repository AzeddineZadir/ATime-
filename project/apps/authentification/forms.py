from django import forms
from django.contrib.auth import authenticate

class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control",'placeholder':"Nom d'utilisateur"}),label='')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control",'placeholder':"Mot de passe"}),label='')

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Votre nom d'utilisateur est incorrecte")
            if not user.check_password(password):
                raise forms.ValidationError("Votre mot de passe est incorrecte")
            if not user.is_active:
                raise forms.ValidationError("Votre compte n'est pas active")
        return super(UserLoginForm, self).clean(*args, **kwargs)

