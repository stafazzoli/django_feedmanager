import datetime
from django.contrib.auth import get_user_model
from django.test import TestCase

from feeds.models import Feed, Post, UserFeed, UserPost

User = get_user_model()


class FeedTestCase(TestCase):
    """This class defines the test suite for the Feed model."""

    def setUp(self) -> None:
        title = 'Simple is Better Than Complex'
        link = 'https://simpleisbetterthancomplex.com/'
        rss = 'https://simpleisbetterthancomplex.com/feed.xml/'
        self.feed = Feed(title=title, link=link, rss=rss)

    def test_model_can_create_a_feed(self):
        old_count = Feed.objects.count()
        self.feed.save()
        new_count = Feed.objects.count()
        return self.assertNotEqual(old_count, new_count)


class UserFeedTestCase(TestCase):
    # test post_save, post_delete signals
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='test@test.com', password='testpassword')
        self.feed = Feed.objects.create(title='test_feed',
                                   link='https://feed.com/',
                                   rss='https://feed.com/feed.xml/'
                                   )
        self.post = Post.objects.create(title='test_post',
                                   description='test_postdesc',
                                   link='https://feed_post.com/',
                                   pub_date=datetime.date.today(),
                                   feed=self.feed)

    def test_model_post_save_userfeed(self):
        userfeed = UserFeed.objects.create(user=self.user, feed=self.feed)
        userpost = UserPost.objects.filter(user=self.user, post__in=self.feed.posts.all())
        self.assertEqual(userpost.count(), userfeed.feed.posts.all().count())

    def test_model_post_delete_userfeed(self):
        userfeed = UserFeed.objects.create(user=self.user, feed=self.feed)
        userpost = UserPost.objects.filter(user=self.user, post__in=self.feed.posts.all())

        userfeed = UserFeed.objects.filter(user=self.user, feed=self.feed).delete()
        self.assertEqual(userpost.count(), 0)
