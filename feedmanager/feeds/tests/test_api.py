import datetime

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.reverse import reverse as api_reverse
from rest_framework.test import APITestCase

from feeds.models import Feed, Post, UserFeed, UserPost

User = get_user_model()


class UserFeedAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='test@test.com', password='testpassword')
        self.user2 = User.objects.create_user(email='test2@test.com', password='testpassword2')
        feed = Feed.objects.create(title='test_feed',
                                   link='https://feed.com/',
                                   rss='https://feed.com/feed.xml/'
                                   )
        self.feed2 = Feed.objects.create(title='test_feed2',
                                         link='https://feed2.com/',
                                         rss='https://feed2.com/feed.xml/'
                                         )
        userfeed = UserFeed.objects.create(user=self.user, feed=feed)

    def test_double_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 2)

    def test_double_feed(self):
        feed_count = Feed.objects.count()
        self.assertEqual(feed_count, 2)

    def test_single_userfeed(self):
        userfeed_count = UserFeed.objects.count()
        self.assertEqual(userfeed_count, 1)

    def test_get_userfeed_list(self):
        """without user authentication"""
        data = {}
        url = api_reverse('feeds:userfeed_listcreate')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_userfeed_list_auth(self):
        self.client.login(email=self.user.email, password='testpassword')
        data = {}
        url = api_reverse('feeds:userfeed_listcreate')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_userfeed(self):
        """without user authentication"""
        data = {"feed": self.feed2.id, "user": self.user.id}
        url = api_reverse('feeds:userfeed_listcreate')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_userfeed_auth(self):
        self.client.login(email=self.user.email, password='testpassword')
        data = {"feed": self.feed2.id, "user": self.user.id}
        url = api_reverse('feeds:userfeed_listcreate')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_userfeed(self):
        """without user authentication"""
        data = {}
        userfeed = UserFeed.objects.first()
        url = api_reverse('feeds:userfeed_delete', kwargs={'pk': userfeed.pk})
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_userfeed_auth_owner(self):
        self.client.login(email=self.user.email, password='testpassword')
        data = {}
        userfeed = UserFeed.objects.first()
        url = api_reverse('feeds:userfeed_delete', kwargs={'pk': userfeed.pk})
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_userfeed_auth_not_owner(self):
        self.client.login(email=self.user2.email, password='testpassword2')
        data = {}
        userfeed = UserFeed.objects.first()
        url = api_reverse('feeds:userfeed_delete', kwargs={'pk': userfeed.pk})
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UserPostListAPITestCase(APITestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(email='test@test.com', password='testpassword')
        self.user2 = User.objects.create_user(email='test2@test.com', password='testpassword2')
        feed = Feed.objects.create(title='test_feed',
                                   link='https://feed.com/',
                                   rss='https://feed.com/feed.xml/'
                                   )
        post = Post.objects.create(title='test_post',
                                   description='test_postdesc',
                                   link='https://feed_post.com/',
                                   pub_date=datetime.date.today(),
                                   feed=feed)
        userpost = UserPost.objects.create(user=self.user, post=post)

    def test_double_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count, 2)

    def test_single_feed(self):
        feed_count = Feed.objects.count()
        self.assertEqual(feed_count, 1)

    def test_single_post(self):
        post_count = Post.objects.count()
        self.assertEqual(post_count, 1)

    def test_single_userpost(self):
        userpost_count = UserPost.objects.count()
        self.assertEqual(userpost_count, 1)

    def test_get_userfeed_list_auth_owner(self):
        self.client.login(email=self.user.email, password='testpassword')
        data = {}
        url = api_reverse('feeds:userpost_list')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)

    def test_get_userfeed_list_auth_not_owner(self):
        self.client.login(email=self.user2.email, password='testpassword2')
        data = {}
        url = api_reverse('feeds:userpost_list')
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 0)

    def test_get_userpost(self):
        """without user authentication"""
        data = {}
        userpost = UserPost.objects.first()
        url = api_reverse('feeds:userpost_detail', kwargs={'pk': userpost.pk})
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_userpost_auth_owner(self):
        self.client.login(email=self.user.email, password='testpassword')
        data = {}
        userpost = UserPost.objects.first()
        url = api_reverse('feeds:userpost_detail', kwargs={'pk': userpost.pk})
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_userpost_auth_not_owner(self):
        self.client.login(email=self.user2.email, password='testpassword2')
        data = {}
        userpost = UserPost.objects.first()
        url = api_reverse('feeds:userpost_detail', kwargs={'pk': userpost.pk})
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_userpost(self):
        """without user authentication"""
        data = {'read': True, 'favourite': True, 'comment': 'commnet_text'}
        userpost = UserPost.objects.first()
        url = api_reverse('feeds:userpost_detail', kwargs={'pk': userpost.pk})
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_userpost_auth_owner(self):
        self.client.login(email=self.user.email, password='testpassword')
        data = {'read': True, 'favourite': True, 'comment': 'commnet_text'}
        userpost = UserPost.objects.first()
        url = api_reverse('feeds:userpost_detail', kwargs={'pk': userpost.pk})
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_userpost_auth_not_owner(self):
        self.client.login(email=self.user2.email, password='testpassword2')
        data = {'read': True, 'favourite': True, 'comment': 'commnet_text'}
        userpost = UserPost.objects.first()
        url = api_reverse('feeds:userpost_detail', kwargs={'pk': userpost.pk})
        response = self.client.get(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

