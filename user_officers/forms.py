from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class RegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("first_name", "last_name", "email", "role", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_active = True
        user.save()
        return user


class CustomUserForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ["first_name", "last_name", "email", "role", "rank", "regiment"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # disable email editing
        self.fields["email"].disabled = True

        role = self.data.get("role") or getattr(self.instance, "role", None)

        if role in ["CTZ", "PRESS", "MLT"]:
            self.fields["rank"].required = False
            self.fields["regiment"].required = False
            self.fields["rank"].widget.attrs["disabled"] = True
            self.fields["regiment"].widget.attrs["disabled"] = True
