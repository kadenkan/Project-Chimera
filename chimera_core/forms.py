from django import forms
from django.contrib.auth import get_user_model
from captcha.fields import CaptchaField

User = get_user_model()

class UserRegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('userName', 'email', 'password')

# class UserLoginForm(forms.ModelForm):
#     captcha = CaptchaField()

#     class Meta:
#         model = User
#         fields = ('userName', 'password')