from django import forms
from chimera_core.models import UserProfileInfo
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserForm(forms.ModelForm):
  password = forms.CharField(widget=forms.PasswordInput())

  class Meta():
    model = User
    fields = ('userName','email', 'password')

class UserProfileInfoForm(forms.ModelForm):
 
 class Meta():
  model = UserProfileInfo
  fields = ('portfolio_site','profile_pic')