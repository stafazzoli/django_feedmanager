from django.contrib import messages
from django.db.models import Q
from django.shortcuts import redirect
from django.views.generic.edit import FormView
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.serializers import ValidationError
from rest_framework.views import APIView

from . import models
from . import serializers
from .forms import ReadFeedsForm
from .permissions import IsOwner
from .tasks import read_feeds


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'userfeed': reverse('feeds:userfeed_listcreate', request=request, format=format),
        'userposts': reverse('feeds:userpost_list', request=request, format=format),
        'userposts_count': reverse('feeds:userposts_count', request=request, format=format),
    })


class UserFeedAPIView(generics.ListCreateAPIView):
    """
    get:
    Returns a list of all the user's feeds.

    post:
    Creates a new feed for the user.
    """
    serializer_class = serializers.UserFeedSerializer

    def perform_create(self, serializer):
        queryset = models.UserFeed.objects.filter(user=self.request.user, feed=serializer.validated_data.get("feed"))
        if queryset.exists():
            raise ValidationError("The fields user and feed must make a unique set.")

        serializer.save(user=self.request.user)

    def get_queryset(self):
        return models.UserFeed.objects.filter(user=self.request.user)


class UserFeedRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    """
    get:
    Return the given the given user's feed.

    destroy:
    Deletes the given user's feed & subsequently deletes all the user's post of that specific feed.
    """
    queryset = models.UserFeed.objects.all()
    serializer_class = serializers.UserFeedSerializer
    permission_classes = (IsOwner,)


class UserPostListAPIView(generics.ListAPIView):
    """
    get:
    Returns a list of posts that user has registered their feed.
    /?q=True  a list of user's favourite posts
    /?q=False a list of user's non-favourite posts
    """
    serializer_class = serializers.UserPostSerializer
    permission_classes = (IsOwner,)

    def get_queryset(self):
        queryset = models.UserPost.objects.filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query is not None:
            queryset = queryset.filter(
                Q(favourite=query)
            ).distinct()
        return queryset


class UserPostRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    retrieve:
    Returns the given user-post detail.

    update:
    Updates the given user-post (read, favorite, comment).
    """
    serializer_class = serializers.UserPostSerializer
    queryset = models.UserPost.objects.all()
    permission_classes = (IsOwner,)


class UserPostCountView(APIView):
    """
    get:
    the number of user's posts.
    /?q=True  the number of user's favourite posts
    /?q=False the number of user's non-favourite posts
    """
    permission_classes = (IsOwner,)

    def get(self, request, format=None):
        queryset = models.UserPost.objects.filter(user=self.request.user)
        query = self.request.GET.get("q")
        if query is not None:
            queryset = queryset.filter(
                Q(favourite=query)
            ).distinct()
        userposts_count = queryset.count()
        content = {'userposts_count': userposts_count}
        return Response(content)


class ReadFeedsView(FormView):
    """
    Reads the feeds' posts from their source and saves into db
    """
    template_name = 'feeds/read_feed.html'
    form_class = ReadFeedsForm

    def form_valid(self, form):
        read_feeds.delay()
        messages.success(self.request, 'We are reading feeds in the background!')
        return redirect('/')
