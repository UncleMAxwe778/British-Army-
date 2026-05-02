from captcha.fields import CaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import request

from .models import Order, News, Request, Operation, RegimentSelection
from user_officers.models import CustomUser


class RegimentSelectionForm(forms.ModelForm):
    class Meta:
        model = RegimentSelection
        fields = ("regiment", "description")


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("name_order", "description_of_order", "data_giving", "user")

    def save(self, commit=True):
        order = super().save(commit=False)
        order.is_active = True
        order.save()
        return order


class NewsForm(forms.ModelForm):

    captcha = CaptchaField(label="Tap a code from the picture")

    class Meta:
        model = News
        fields = ("news_name", "description_of_news", "rate_for_news", "data_giving")

    def save(self, commit=True):
        news = super().save(commit=False)
        news.is_active = True
        news.save()
        return news



class RequestForm(forms.ModelForm):

    class Meta:
        model = Request
        fields = ("title", "description", "assigned_officer")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["assigned_officer"].queryset = CustomUser.objects.filter(
            role="MLT",
            rank__in=["COL", "BRIG","MG", "LG", "GEN"]
        )

class RequestForArmyForm(forms.ModelForm):

    class Meta:
        model = Request
        fields = ("title", "description", "assigned_officer", "document")
        widgets = {
            'document': forms.FileInput(attrs={
                'accept': 'image/*',
                'class': 'form-control'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["assigned_officer"].queryset = CustomUser.objects.filter(
            role="MLT",
            rank__in=["COL", "BRIG","MG", "LG", "GEN"]
        )


class OperationForm(forms.ModelForm):

    class Meta:
        model = Operation
        fields = ("name","description", "region", "status")

    def save(self, commit=True):
        operation = super().save(commit=False)
        operation.is_active = True
        operation.save()
        return operation
