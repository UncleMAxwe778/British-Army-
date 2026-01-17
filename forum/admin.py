from django.contrib import admin
from .models import News

@admin.register(News)
class AdminNews(admin.ModelAdmin):
    list_display = ("id","news_name", "description_of_news", "rate_for_news", "published_by", "data_giving")
    list_editable = ("description_of_news","data_giving")
    list_filter = ("news_name", "description_of_news", "rate_for_news", "published_by", "data_giving")



