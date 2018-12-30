from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('userName', 'email', 'password')
