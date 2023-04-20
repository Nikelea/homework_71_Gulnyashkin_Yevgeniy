from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from .models import Profile, Follower


class ProfileInline(admin.StackedInline):
   model = Profile
   fields = ['sex', 'phone', 'avatar', 'about']


class ProfileAdmin(UserAdmin):
   inlines = [ProfileInline]

User = get_user_model()
admin.site.unregister(User)
admin.site.register(User, ProfileAdmin)


admin.site.register(Follower)
