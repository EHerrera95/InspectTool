from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import InputModel, IGModel

class InputForm(forms.ModelForm):
    class Meta:
        model = InputModel
        fields = ['criteria', 'filename']

class InspectionGuideForm(forms.ModelForm):
     class Meta:
        model = IGModel
        fields = ['criteria']


class CreateUserForm(UserCreationForm): 
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

        widgets = {
            'username' : forms.TextInput(attrs= {'placeholder' : 'Username'}),
            'email' : forms.TextInput(attrs= {'placeholder' : 'Email'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder' : 'Enter Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder' : 'Re-Enter Password'})
