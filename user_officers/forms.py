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

        role = self.data.get("role") or getattr(self.instance, "role", None)

        if role == "CTZ":
            self.fields.pop("rank", None)
            self.fields.pop("regiment", None)
        if role == "PRESS":
            self.fields.pop("rank", None)
            self.fields.pop("regiment", None)
        print("FIELDS AFTER:", self.fields.keys())