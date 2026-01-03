from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Order, News



class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("name_order", "description_of_order", "data_giving", "rate_for_order", "user")

    def save(self, commit=True):
        order = super().save(commit=False)
        order.is_active = True
        order.save()
        return order




class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ("news_name", "description_of_news", "rate_for_news", "published_by", "data_giving")

    def save(self, commit=True):
        news = super().save(commit=False)
        news.is_active = True
        news.save()
        return news

