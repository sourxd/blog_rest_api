from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from blog.models import User, Subscription, Post, Blog

admin.site.register(User, UserAdmin)
admin.site.register(Blog)
admin.site.register(Post)
admin.site.register(Subscription)
