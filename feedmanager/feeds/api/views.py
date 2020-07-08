from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.serializers import ValidationError

from feeds import models
from feeds.api import serializers
from feeds.api.permissions import IsOwner


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'userfeed': reverse('feeds:userfeed_list_create', request=request, format=format),
        'userposts': reverse('feeds:userpost_all_list', request=request, format=format),
    })


class UserFeedAPIView(generics.ListCreateAPIView):
    """
    get:
    Returns a list of the user's all feeds.

    post:
    Creates a new feed for the user.
    """
    serializer_class = serializers.UserFeedSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return models.UserFeed.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        queryset = models.UserFeed.objects.filter(user=self.request.user, feed=serializer.validated_data.get("feed"))
        if queryset.exists():
            raise ValidationError("The fields user and feed must make a unique set.")

        serializer.save(user=self.request.user)


class UserFeedRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    """
    get:
    Return the given the given user's feed.

    destroy:
    Deletes the given user's feed & subsequently deletes all the user's post of that specific feed.
    """
    queryset = models.UserFeed.objects.all()
    serializer_class = serializers.UserFeedSerializer
    permission_classes = (IsAuthenticated, IsOwner,)


class UserPostListAPIView(generics.ListAPIView):
    """
    get:
    Returns a list of posts of all feed that user has registered for.
    /?fav=True/False a list of user's favourite/non-favourite posts
    """
    serializer_class = serializers.UserPostSerializer
    permission_classes = (IsAuthenticated, IsOwner,)

    def get_queryset(self):
        queryset = models.UserPost.objects.filter(user=self.request.user)
        fav = self.request.GET.get("fav")
        if fav is not None:
            queryset = queryset.filter(is_favourite=fav)
        return queryset


class UserPost_ByFeedListAPIView(generics.ListAPIView):
    """
    get:
    Returns a list of posts of a specific feed that user has registered for.
    /?fav=True/False a list of user's favourite/non-favourite posts in a specific feed
    """
    serializer_class = serializers.UserPostSerializer
    permission_classes = (IsAuthenticated, IsOwner,)

    def get_queryset(self):
        queryset = models.UserPost.objects.filter(user=self.request.user, post__feed=self.kwargs.get("pk"))
        fav = self.request.GET.get("fav")
        if fav is not None:
            queryset = queryset.filter(is_favourite=fav)
        return queryset


class UserPostRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """
    retrieve:
    Returns the given user-post detail.

    update:
    Updates the given user-post (is_read, is_favorite, comment).
    """
    serializer_class = serializers.UserPostSerializer
    queryset = models.UserPost.objects.all()
    permission_classes = (IsAuthenticated, IsOwner,)
