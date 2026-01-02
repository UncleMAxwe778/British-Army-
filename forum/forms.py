from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Private, Order, Steamer


class RecruitForm(forms.ModelForm):
    class Meta:
        model = Private
        fields = ("first_name_private", "last_name_private", "call_sign", "rank", "biography", "university_education", "steamer")

    def save(self, commit=True):
        recruit = super().save(commit=False)
        recruit.is_active = True
        recruit.save()
        return recruit

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("name_order", "description_of_order", "data_giving", "rate_for_order", "user")

    def save(self, commit=True):
        order = super().save(commit=False)
        order.is_active = True
        order.save()
        return order

class SteamerForm(forms.ModelForm):
    class Meta:
        model = Steamer
        fields = ("first_name_steamers", "last_name_steamers", "call_sign", "rank", "biography", "combat_experience")

    def save(self, commit=True):
        steamer = super().save(commit=False)
        steamer.is_active = True
        steamer.save()
        return steamer
