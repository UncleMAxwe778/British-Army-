from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.core.cache import cache
from django.http import JsonResponse
from django.db.models import Q
import json

from .forms import OrderForm, NewsForm, RequestForm, OperationForm, RegimentSelectionForm
from .models import Order, News, Request, MessageList, ReviewerOfRequest, Operation, CircleData, RegimentSelection
from .filters import PrivateFilter
import logging
from user_officers.models import CustomUser

logger = logging.getLogger(__name__)

# Index
def greetings_view(request):
    return render(request, "forum/index.html")

# Home
def home(request):
    news = News.objects.all()
    return render(request, 'forum/home.html', {'news': news})

#Orders

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
    return render(request, 'forum/create_order.html', {'form': form})

@login_required
def list_of_all_orders(request):
    if not request.user.only_for_military():
        return HttpResponseForbidden("You don't have permission to those actions.")
    orders = Order.objects.all()
    return render(request, 'forum/all_order_view.html', {'orders': orders})


# Regiment-selection
@login_required
def create_selection(request):
    if not request.user.staff_for_create():
        return HttpResponseForbidden("You don't have permission to those actions")

    form = RegimentSelectionForm()

    if request.method == "POST":
        form = RegimentSelectionForm(request.POST)
        if form.is_valid():
            selection = form.save(commit=False)
            selection.published_by = request.user
            selection.save()
            messages.success(request, "The selection of regiment was successfully created")
            return redirect("forum:create_selection")
    return render(request, 'forum/create_selection.html', {'form': form})


@login_required
def sign_up_selection(request, selection_id):
    selection = get_object_or_404(RegimentSelection, id=selection_id)

    if selection.is_full():
        messages.error(request, "This selection is already full!")
    elif request.user in selection.recruits.all():
        messages.warning(request, "You already signed up for this selection!")
    else:
        selection.recruits.add(request.user)
        messages.success(request, f"You signed up for {selection.regiment}!")

    return redirect('forum:selection_list')

@login_required
def selection_list(request):
    if not request.user.only_for_military():
        return HttpResponseForbidden("You don't have permission to those actions.")

    selections = RegimentSelection.objects.all()
    return render(request, 'forum/all_selections.html', {'selections': selections})

@login_required
def remove_recruit_from_selection(request, selection_id):
    selection = get_object_or_404(RegimentSelection, id=selection_id)

    if request.user in selection.recruits.all():
        selection.recruits.remove(request.user)
        messages.success(request, f"You're leaved from the selection of regiment {selection.regiment}")
    else:
        messages.warning(request, "You are not signed up for this selection!")

    return redirect('forum:selection_list')


@login_required
def delete_selection(request, selection_id):
    if not request.user.staff_for_create():
        return HttpResponseForbidden("You don't have permission to those actions")

    RegimentSelection.objects.filter(id=selection_id, published_by=request.user).delete()
    messages.success(request, "You're deleted the selection")
    return redirect('forum:selection_list')


# News Reporting
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
    return render(request, 'forum/all_news.html', {'news': news})


def news_by_detail(request, news_id):
    news = get_object_or_404(News, id=news_id)
    return render(request, 'forum/news_by_detail.html', {'news': news})




#Messages
@login_required
def unread_notifications(request):
    messages = MessageList.objects.filter(
        receiver=request.user,
        is_read=False
    ).order_by('-data_giving')
    return render(request, "forum/unread_notifications.html", {"mesages": messages})


@require_POST
def mark_notification_read(request, pk):
    if request.user.is_authenticated:
        try:
            msg = MessageList.objects.get(pk=pk, receiver=request.user)
            msg.is_read = True
            msg.save(update_fields=['is_read'])
            return JsonResponse({'success': True})
        except MessageList.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Message not found'}, status=404)
    return JsonResponse({'success': False, 'error': 'Not authenticated'}, status=403)


#Requests
@login_required
def request_as_a_user(request):
    form = RequestForm()

    if request.method == "POST":
        form = RequestForm(request.POST)
        if form.is_valid():
            requestt = form.save(commit=False)
            requestt.creator = request.user
            requestt.save()
            messages.success(request, "Your request is successfully issued")
            return redirect("forum:list_of_requests")
    return render(request, 'forum/create_request.html', {'form': form})


@login_required
def list_of_requests(request):
    if request.user.is_staff:
        requests_qs = Request.objects.all()
    else:
        requests_qs = Request.objects.filter(creator=request.user)

    return render(request, 'forum/list_of_requests.html', {'requests': requests_qs})


@login_required
def add_request_to_review_list(request, request_id):
    if not request.user.staff_for_create():
        return HttpResponseForbidden("You don't have permission for this action")

    req = Request.objects.get(id=request_id)
    ReviewerOfRequest.objects.create(request=req, reviewer=request.user)

    messages.success(request, "Request added to your review list")
    return redirect("forum:list_of_requests")


@login_required
def review_dashboard(request):
    if not request.user.staff_for_create():
        return HttpResponseForbidden("You don't have permission for this action")

    reviews = ReviewerOfRequest.objects.filter(reviewer=request.user).select_related("request")
    return render(request, 'forum/review_dashboard.html', {'reviews': reviews})


@login_required
def review_action(request, request_id):
    if not request.user.staff_for_create():
        return HttpResponseForbidden("You don't have permission for this action")

    if request.method == "POST":
        import json
        try:
            data = json.loads(request.body)
            decision_value = data.get("decision")
        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON"}, status=400)

        try:
            rqst = Request.objects.get(id=request_id)
        except Request.DoesNotExist:
            return JsonResponse({"error": "Request not found"}, status=404)


        reviewer_obj, created = ReviewerOfRequest.objects.get_or_create(
            request=rqst,
            reviewer=request.user,
            defaults={"decision": decision_value}
        )

        if not created:
            reviewer_obj.decision = decision_value
            reviewer_obj.reviewed_at = timezone.now()
            reviewer_obj.save()

        rqst.current_status = reviewer_obj
        rqst.save()

        return JsonResponse({"new_status": reviewer_obj.decision})
    return JsonResponse({"error": "Invalid request method"}, status=405)



#Operations
@login_required
def make_the_operation(request):
    if not request.user.staff_for_create():
        return HttpResponseForbidden("You don't have permission to those actions.")

    form = OperationForm()

    if request.method == "POST":
        form = OperationForm(request.POST)
        if form.is_valid():
            operation = form.save(commit=False)
            operation.created_by = request.user
            operation.save()
            messages.success(request, "Operation has been added")
            return redirect("forum:list_of_operations")
    return render(request, 'forum/create_operation.html', {'form': form})

@login_required
def list_of_operations(request):
    if not request.user.staff_for_create():
        return HttpResponseForbidden("You don't have permission to view those actions.")

    operations = Operation.objects.all()
    return render(request, 'forum/view_list_of_operations.html', {'operations': operations})

@login_required
def delete_operation(request, operation_id):
    Operation.objects.filter(id=operation_id, created_by=request.user).delete()
    return redirect('forum:list_of_operations')

@login_required
def operation_edit(request, operation_id):
    if not request.user.staff_for_create():
        return HttpResponseForbidden("You don't have permission to those actions.")

    operation = get_object_or_404(Operation, id=operation_id)

    if request.method == 'POST':
        form = OperationForm(request.POST, instance=operation)
        if form.is_valid():
            form.save()
            messages.success(request, 'Operation has been updated successfully')
        else:
            messages.error(request, 'Please correct errors')
    else:
        form = OperationForm(instance=operation)
    return render(request, 'forum/edit_operation.html', {'form': form})



#Circles
@login_required
def create_circle(request):
    if request.method == "POST":
        data = json.loads(request.body)
        x = data.get("x")
        y = data.get("y")
        operation_id = data.get("operation_id")
        operation = Operation.objects.get(id=operation_id)

        circle = CircleData.objects.create(
            operation=operation,
            x=x,
            y=y
        )

        return JsonResponse({
            "id": circle.id,
            "operation": circle.operation.name,
            "x": circle.x,
            "y": circle.y
        })
    return JsonResponse({"error": "Invalid request"}, status=400)


@login_required
def get_circles(request):
    circles = CircleData.objects.all()
    data = []
    for c in circles:
        data.append({
            "id": c.id,
            "operation_name":c.operation.name,
            "x": c.x,
            "y": c.y
        })
    return JsonResponse(data, safe=False)


@login_required
def delete_circle(request, circle_id):
    if request.method == "DELETE":
        try:
            circle = CircleData.objects.get(id=circle_id)
            circle.delete()
            return JsonResponse({"success": True})
        except CircleData.DoesNotExist:
            return JsonResponse({"error": "Circle not found"}, status=404)
    return JsonResponse({"error": "Invalid request"}, status=400)

@login_required
def map_of_uk_view(request):
    if not request.user.staff_for_create():
        return HttpResponseForbidden("You don't have permission to those actions.")

    operations = Operation.objects.all()
    circles = CircleData.objects.all()
    return render(request, "forum/uk_map.html", {"operations": operations, "circles": circles})








