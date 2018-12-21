from django import forms
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField

User = get_user_model()

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    captcha = CaptchaField()
    class Meta():
        model = User
        fields = ('userName','email', 'password')
