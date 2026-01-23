from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from ninja import NinjaAPI
from ninja.security import django_auth

from .models import News
from forum.schemas import Newsout

api_ninja =NinjaAPI()


@api_ninja.get("/", response=list[Newsout])
def list_news(request):
    return News.objects.all()


@api_ninja.post("/", response=Newsout, auth=django_auth)
@csrf_exempt
def create_news(request, data: Newsout):
    news = News.objects.create(
        news_name= data.news_name,
        description_of_news= data.description_of_news,
        rate_for_news= data.rate_for_news,
        published_by=request.user,
        data_giving= data.data_giving
    )
    return news


@api_ninja.delete("/{news_id}", auth=django_auth)
@csrf_exempt
def delete_news(request, news_id: int):
    news = get_object_or_404(News, id=news_id)
    news.delete()
    return {"success": True}


