from django.db.models import Q
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from . import models


@receiver(post_save, sender=models.UserFeed)
def create_userposts(sender, instance, created, **kwargs):
    """ creates UserPosts when a new user is added to a Feed """
    if created:
        userpost_list = []
        for p in instance.feed.posts.all():
            userpost = models.UserPost(user=instance.user, post=p)
            userpost_list.append(userpost)

        models.UserPost.objects.bulk_create(userpost_list)


@receiver(post_delete, sender=models.UserFeed)
def delete_userposts(sender, instance, **kwargs):
    """ deletes UserPosts when a new user is removed from a Feed """

    userposts = models.UserPost.objects.filter(Q(user=instance.user) & Q(post__in=instance.feed.posts.all()))

    for up in userposts:
        up.delete()
