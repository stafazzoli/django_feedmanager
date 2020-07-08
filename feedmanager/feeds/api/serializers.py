from rest_framework import serializers

from feeds import models


class UserFeedSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email')
    feed_title = serializers.CharField(source='feed.title', read_only=True)

    class Meta:
        model = models.UserFeed
        fields = ('id', 'user', 'feed', 'feed_title',)
        read_only_fields = ('user', 'feed_title',)


class UserPostSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.email', read_only=True)
    post_feed_title = serializers.CharField(source='post.feed.title', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)
    post_desc = serializers.CharField(source='post.description', read_only=True)
    post_link = serializers.URLField(source='post.link', read_only=True)
    post_pub_date = serializers.DateTimeField(source='post.pub_date', read_only=True)

    class Meta:
        model = models.UserPost
        fields = ('id', 'user', 'is_read', 'is_favourite', 'comment',
                  'post_feed_title', 'post_title', 'post_desc', 'post_link', 'post_pub_date',
                  )
        read_only_fields = ('user', 'post_feed_title', 'post_title', 'post_desc', 'post_pub_date',)
