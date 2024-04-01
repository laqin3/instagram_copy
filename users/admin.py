from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import InstagramCopyUser, FriendRequest

# Register your models here.
admin.site.register(InstagramCopyUser, UserAdmin)
admin.site.register(FriendRequest)
