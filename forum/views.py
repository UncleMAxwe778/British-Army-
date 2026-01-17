from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.cache import cache

from .forms import OrderForm, NewsForm
from .models import Order, News, BusketCheck
from .filters import PrivateFilter
import logging


logger = logging.getLogger(__name__)


def home(request):
    order_list = Order.objects.all()
    paginator = Paginator(order_list , 1)
    page_number = request.GET.get('page', 1)
    try:
        orders = paginator.page(page_number)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        orders = paginator.page(1)
    return render(request, 'forum/home.html', {'orders': orders})

@login_required
def make_order_for_private(request):

    if not request.user.staff_for_create():
        return HttpResponseForbidden("You don't have permission to create orders.")

    form = OrderForm()

    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.save()
            messages.success(request, "Order has been added")
            return redirect("forum:make_order_for_soldier")
    return render(request, 'forum/make_order_for_recruit.html', {'form': form})

def list_of_all_orders(request):
    orders = Order.objects.all()
    return render(request,'forum/all_order_view.html', {'orders': orders} )



@login_required
def create_news_of_british_army(request):

    if not request.user.can_create_news():
        return HttpResponseForbidden("You don't have permission to create news.")

    form = NewsForm()

    if request.method == "POST":
        form = NewsForm(request.POST)
        if form.is_valid():
            news = form.save(commit=False)
            news.published_by = request.user
            news.save()
            messages.success(request, "The layer of magazine news has been added")
            return redirect("forum:watching_news_of_british_army")
    return render(request, 'forum/create_news_of_british_army.html', {'form': form})

def watching_news_of_british_army(request):
    cache_key = "news_list"
    news = cache.get(cache_key)

    if not news:
        logger.warning("Bases from BD")
        news = News.objects.all()
        cache.set(cache_key, news, timeout=300)
    else:
        logger.warning("Bases from Cache")
    return render(request,'forum/all_news.html', {'news': news})

def news_by_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    return render(request,'forum/news_by_detail.html', {'news': news})

@login_required
def add_news_to_check_bucket(request, news_id):

    if not request.user.staff_for_create():
        return HttpResponseForbidden("You don't have permission to this action")

    news = News.objects.get(id=news_id)
    BusketCheck.objects.create(check_info_news=news, published_by=request.user)
    messages.success(request, "The object news's was added to check bucket")
    return redirect("forum:watching_news_of_british_army")


@login_required
def bucket_check_view(request):
    news = BusketCheck.objects.filter(published_by=request.user).select_related("check_info_news")
    return render(request, 'forum/bucket.html', {'news': news})



