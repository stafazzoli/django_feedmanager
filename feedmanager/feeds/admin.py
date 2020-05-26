from django.contrib import admin

from . import models


class UserInLine(admin.TabularInline):
    model = models.UserFeed


class FeedAdmin(admin.ModelAdmin):
    inlines = [
        UserInLine,
    ]


admin.site.register(models.Post)
admin.site.register(models.UserFeed)
admin.site.register(models.Feed, FeedAdmin)
admin.site.register(models.UserPost)
