from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "rank", "role", "regiment", "password1", "password2" )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        user.save()
        return user


class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "rank", "regiment", "role"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        print(self.fields, 'FIELDS DATA')
        self.fields['email'].disabled = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.role == "CTZ":
            self.fields.pop('rank')
            self.fields.pop('regiment')
        if self.instance and self.instance.role == "PRESS":
            self.fields.pop('rank')
            self.fields.pop('regiment')