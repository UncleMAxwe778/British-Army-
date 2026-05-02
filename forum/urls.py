from django.urls import path
from .views import ( home, make_order_for_private, list_of_all_orders, create_news_of_british_army,
                    watching_news_of_british_army,
                    news_by_detail, unread_notifications, request_as_a_user, list_of_requests,
                    add_request_to_review_list,
                    review_dashboard,
                    mark_notification_read, review_action, map_of_uk_view, create_circle, get_circles, delete_circle, make_the_operation,
                    list_of_operations, delete_operation, operation_edit, selection_list, sign_up_selection, create_selection, remove_recruit_from_selection, delete_selection, request_as_a_user_for_join_army
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
    path('request-as-a-user-for-join-army/', request_as_a_user_for_join_army, name='request_as_a_user_for_join_army'),
    path('list-of-requests/', list_of_requests, name='list_of_requests'),
    path('list-of-requests/add-request-to-review-list/<int:request_id>/', add_request_to_review_list, name='add_request_to_review_list'),
    path('review-dashboard/', review_dashboard, name='review_dashboard'),
    path('review-dashboard/review-action/<int:request_id>/', review_action, name='review_action'),
    path('uk-map/', map_of_uk_view, name='map_of_uk_view'),
    path('create-circle/', create_circle, name='create_circle'),
    path('get-circles/', get_circles, name='get_circles'),
    path('delete-circle/<int:circle_id>/', delete_circle, name='delete_circle'),
    path('operation/<int:operation_id>/delete/', delete_operation, name='delete_operation'),
    path('create-operation/', make_the_operation, name='make_the_operation'),
    path('operations/', list_of_operations, name="list_of_operations"),
    path('operation/<int:operation_id>/edit/', operation_edit, name='operation_edit'),
    path('selections/', selection_list, name='selection_list'),
    path('selections/sign-up/<int:selection_id>', sign_up_selection, name='sign_up_selection'),
    path('create-selection/', create_selection, name='create_selection'),
    path('selections/remove/<int:selection_id>/', remove_recruit_from_selection, name='remove_recruit_from_selection'),
    path('selection/<int:selection_id>/delete/', delete_selection, name='delete_selection'),
]
