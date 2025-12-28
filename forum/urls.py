from django.urls import path
from .views import home, add_steamer, private_view, add_recruit_view, make_order_for_private, show_all_privates, list_of_all_orders


app_name = 'forum'

urlpatterns = [
    path('home-page/', home, name='home_page' ),
    path('steamer-create/', add_steamer, name='add_steamer'),
    path('private/<int:private_id>', private_view, name='private_view'),
    path('all-privates-view/', show_all_privates, name='all_privates_view'),
    path('add-create-view/', add_recruit_view, name='add_private_view'),
    path('make-order-for-soldier/', make_order_for_private, name='make_order_for_soldier'),
    path('list-of-all-orders/', list_of_all_orders, name='list_of_all_orders')
]
