from django.contrib.auth import get_user_model
from django.test import TestCase

from feeds.models import Feed

User = get_user_model()


class FeedTestCase(TestCase):
    """This class defines the test suite for the Feed model."""

    def setUp(self) -> None:
        self.title = 'Simple is Better Than Complex'
        self.link = 'https://simpleisbetterthancomplex.com/'
        self.rss = 'https://simpleisbetterthancomplex.com/feed.xml/'
        self.feed = Feed(title=self.title, link=self.link, rss=self.rss)

    def test_model_can_create_a_feed(self):
        old_count = Feed.objects.count()
        self.feed.save()
        new_count = Feed.objects.count()
        return self.assertNotEqual(old_count, new_count)


class UserFeedModel(TestCase):
    # test post_save, post_delete signals
    pass
