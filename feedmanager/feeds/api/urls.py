from django.urls import path

from feeds.api import views

app_name = 'feeds'

urlpatterns = [
    path('', views.api_root, name='api_root'),
    path('v1/userfeeds/', views.UserFeedAPIView.as_view(), name='userfeed_list_create'),
    path('v1/userfeed/<int:pk>', views.UserFeedRetrieveDestroyAPIView.as_view(), name='userfeed_retreive_delete'),
    path('v1/userposts/', views.UserPostListAPIView.as_view(), name='userpost_all_list'),
    path('v1/userposts/feed/<int:pk>', views.UserPost_ByFeedListAPIView.as_view(), name='userpost_feed_list'),
    path('v1/userpost/<int:pk>/', views.UserPostRetrieveUpdateAPIView.as_view(), name='userpost_detail'),
]
