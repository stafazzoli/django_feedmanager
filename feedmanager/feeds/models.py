from django.contrib.auth.models import User
from django.db import models


class Feed(models.Model):
    title = models.CharField(max_length=30, unique=True)
    link = models.URLField(unique=True)
    rss = models.URLField(unique=True)
    last_pub_date = models.DateTimeField(blank=True, null=True)
    users = models.ManyToManyField(User, through='UserFeed', related_name='feeds', blank=True, editable=True)

    def __str__(self):
        return self.title


class UserFeed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    feed = models.ForeignKey(Feed, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'feed')

    def __str__(self):
        return f"user: {self.user.username} - feed: {self.feed.title}"


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    link = models.URLField(unique=True)
    pub_date = models.DateTimeField()
    feed = models.ForeignKey(Feed, related_name='posts', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class UserPost(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='users', on_delete=models.CASCADE)
    read = models.BooleanField(default=False)
    favourite = models.BooleanField(default=False)
    comment = models.TextField(null=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"user:  {self.user.username} - post: {self.post.title}"
