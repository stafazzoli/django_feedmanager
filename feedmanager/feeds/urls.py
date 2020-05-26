from django.urls import path

from . import views

app_name = 'feeds'

urlpatterns = [
    path('', views.api_root, name='api_root'),
    path('api/v1/userfeeds/', views.UserFeedAPIView.as_view(), name='userfeed_listcreate'),
    path('api/v1/userfeed/<int:pk>', views.UserFeedRetrieveDestroyAPIView.as_view(), name='userfeed_delete'),
    path('api/v1/userposts/', views.UserPostListAPIView.as_view(), name='userpost_list'),
    path('api/v1/userposts_count/', views.UserPostCountView.as_view(), name='userposts_count'),
    path('api/v1/userpost/<int:pk>/', views.UserPostRetrieveUpdateAPIView.as_view(), name='userpost_detail'),

    path('readfeeds/', views.ReadFeedsView.as_view(), name='read_feeds'),
]
