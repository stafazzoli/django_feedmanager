from datetime import datetime
from time import mktime

import feedparser
import pytz
from celery import shared_task

from . import models


def add_userpost(users, posts):
    userpost_list = []
    for user in users:
        for post in posts:
            userpost = models.UserPost(user=user, post=post)
            userpost_list.append(userpost)
    models.UserPost.objects.bulk_create(userpost_list)


@shared_task
def read_feeds():
    for feed in models.Feed.objects.all():
        try:
            feed_to_parse = feedparser.parse(feed.rss)

            post_list = []
            post_count = 0
            tz = pytz.timezone('UTC')
            feed_pub_date = datetime.fromtimestamp(mktime(feed_to_parse.feed.get("published_parsed")), tz=tz)

            if feed.last_pub_date is None or feed_pub_date != feed.last_pub_date:
                for feed_item in feed_to_parse.entries:
                    feed_item_pubdate = datetime.fromtimestamp(mktime(feed_item.get("published_parsed")), tz=tz)
                    if feed.last_pub_date is None or feed_item_pubdate > feed.last_pub_date:
                        post = models.Post(
                            title=feed_item.get("title", "No title"),
                            link=feed_item.get("link", "No link"),
                            description=feed_item.get("description", "No desc"),
                            pub_date=datetime.fromtimestamp(mktime(feed_item.get("published_parsed")), tz=tz),
                            feed=feed,
                        )
                        post.save()
                        post_list.append(post)
                        post_count += 1

                feed.last_pub_date = feed_pub_date
                feed.save()

                add_userpost(feed.users.all(), post_list)

        except Exception as e:
            print(f"An error has occurred when parsing the feed of {feed.title}", e)
        finally:
            print(f"The number of new posts entered for {feed.title}: {post_count}")
