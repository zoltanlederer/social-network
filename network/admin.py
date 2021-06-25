from django.contrib import admin
from .models import User, Posts, Follow


class PostsAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created')


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'following')


# Register your models here.
admin.site.register(User)
admin.site.register(Posts, PostsAdmin)
admin.site.register(Follow, FollowAdmin)