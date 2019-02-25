from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password=forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('userName', 'email', 'password')

    def clean(self):
        cleaned_data = super(UserRegForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Passwords do not match!"
            )
