from django.urls import path
from .views import (home, make_order_for_private, list_of_all_orders, create_news_of_british_army, watching_news_of_british_army,
                    add_news_to_check_bucket, bucket_check_view, news_by_detail)


app_name = 'forum'

urlpatterns = [
    path('home-page/', home, name='home_page' ),
    path('make-order-for-soldier/', make_order_for_private, name='make_order_for_soldier'),
    path('list-of-all-orders/', list_of_all_orders, name='list_of_all_orders'),
    path('create-news-of-british-army/', create_news_of_british_army, name='create_news_of_british_army'),
    path('watching-news-of-british-army/', watching_news_of_british_army, name='watching_news_of_british_army'),
    path('watching-news-of-british-army/<int:news_id>/', news_by_detail, name='news_by_detail'),
    path('watching-news-of-british-army/add_news_to_check_bucket/<int:news_id>/', add_news_to_check_bucket, name='add_news_to_check_bucket'),
    path('bucket-check-view/', bucket_check_view, name='bucket_check_view')
]
