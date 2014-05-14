from django.contrib import admin
from .models import Profile
from .models import Community
from .models import Tos

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
	list_display = ['name']

@admin.register(Tos)
class TosAdmin(admin.ModelAdmin):
	list_display = ['version']
