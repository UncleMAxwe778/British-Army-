from django.urls import path
from .views import (home, make_order_for_private, list_of_all_orders, create_news_of_british_army,
                    watching_news_of_british_army,
                    news_by_detail, unread_notifications, request_as_a_user, list_of_requests,
                    add_request_to_review_list,
                    review_dashboard,
                    mark_notification_read, review_action, map_of_uk_view, create_circle, make_the_operation
                    )


app_name = 'forum'

urlpatterns = [
    path('home-page/', home, name='home_page'),
    path('make-order-for-soldier/', make_order_for_private, name='make_order_for_soldier'),
    path('list-of-all-orders/', list_of_all_orders, name='list_of_all_orders'),
    path('create-news-of-british-army/', create_news_of_british_army, name='create_news_of_british_army'),
    path('watching-news-of-british-army/', watching_news_of_british_army, name='watching_news_of_british_army'),
    path('watching-news-of-british-army/<int:news_id>/', news_by_detail, name='news_by_detail'),
    path('notifications/unread/', unread_notifications, name='unread_notifications'),
    path('notifications/read/<int:pk>/', mark_notification_read, name='mark_notification_read'),
    path('request-as-a-user/', request_as_a_user, name='request_as_a_user'),
    path('list-of-requests/', list_of_requests, name='list_of_requests'),
    path('list-of-requests/add-request-to-review-list/<int:request_id>/', add_request_to_review_list, name='add_request_to_review_list'),
    path('review-dashboard/', review_dashboard, name='review_dashboard'),
    path('review-dashboard/review-action/<int:request_id>/', review_action, name='review_action'),
    path('uk-map/', map_of_uk_view, name='map_of_uk_view'),
    path('create-circle/', create_circle, name='create_circle'),
    path('create-operation/', make_the_operation, name='make_the_operation')
]
