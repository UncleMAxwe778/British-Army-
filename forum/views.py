from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from .forms import RecruitForm, OrderForm, SteamerForm
from .models import Steamer, Private, Order
from .filters import PrivateFilter

def home(request):
    steamers = Steamer.objects.all()
    privates_list = Private.objects.all()
    paginator = Paginator(privates_list , 1)
    page_number = request.GET.get('page', 1)
    try:
        privates = paginator.page(page_number)
    except EmptyPage:
        privates = paginator.page(paginator.num_pages)
    except PageNotAnInteger:
        privates = paginator.page(1)
    return render(request, 'forum/home.html', {'steamers': steamers, 'privates': privates})

def private_view(request, private_id):
    private = get_object_or_404(Private, id=private_id)
    return render(request, 'forum/private_view.html', {'private': private})

def show_all_privates(request):
    privates = Private.objects.all()
    my_filter = PrivateFilter(request.GET, queryset=privates)
    privates = my_filter.qs
    return render(request,'forum/all_privates_view.html', {'privates': privates} )

def add_recruit_view(request):
    form = RecruitForm()
    if request.method == "POST":
        form = RecruitForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.save()
            messages.success(request, "Recruits has been added")
            return redirect("forum:add_private_view")
    return render(request, 'forum/create_private.html', {'form': form})

@login_required
def make_order_for_private(request):

    if not request.user.can_create_orders():
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


def add_steamer(request):
    form = SteamerForm()
    if request.method == "POST":
        form = SteamerForm(request.POST)
        if form.is_valid():
            material = form.save(commit=False)
            material.save()
            messages.success(request, "Steamer has been added")
            return redirect("forum:add_steamer")
    return render(request, 'forum/create_steamer.html', {'form': form})


def list_of_all_orders(request):
    orders = Order.objects.all()
    return render(request,'forum/all_order_view.html', {'orders': orders} )
