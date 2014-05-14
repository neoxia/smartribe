from django.contrib import admin
from .models import Profile
from .models import Community


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
	list_display = ['name']
