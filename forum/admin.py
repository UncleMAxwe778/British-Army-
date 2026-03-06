from django.contrib import admin
from .models import News, Operation, CircleData, Order, RegimentSelection

@admin.register(News)
class AdminNews(admin.ModelAdmin):
    list_display = ("id","news_name", "description_of_news", "rate_for_news", "published_by", "data_giving")
    list_editable = ("description_of_news","data_giving")
    list_filter = ("news_name", "description_of_news", "rate_for_news", "published_by", "data_giving")


@admin.register(Operation)
class AdminOperation(admin.ModelAdmin):
    list_display = ("id","name", "description", "region", "status", "created_by", "created_at")
    list_editable = ("region", "status")
    list_filter = ("region", "status", "created_by", "created_at")


@admin.register(CircleData)
class AdminCircleData(admin.ModelAdmin):
    list_display = ("id", "operation", "x", "y", "timestamp")
    list_editable = ("operation",)
    list_filter = ("operation", "x", "y", "timestamp")

@admin.register(Order)
class AdminOrder(admin.ModelAdmin):
    list_display = ("id", "name_order", "description_of_order", "user", "data_giving")
    list_editable = ("name_order", "description_of_order")
    list_filter = ("name_order", "description_of_order", "user", "data_giving")

@admin.register(RegimentSelection)
class AdminRegimentSelection(admin.ModelAdmin):
    list_display = ( "published_by", "id", "regiment", "description", "date_giving", "max_recruits")
    list_editable = ( "max_recruits", "regiment",)
    list_filter = ( "published_by", "regiment", "description", "date_giving", "max_recruits")




