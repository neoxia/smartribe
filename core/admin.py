from django.contrib import admin
from core.models import Member
from .models import Profile
from .models import Community
from .models import Tos
from .models import Skill
from .models import Request
from .models import Offer
from .models import PasswordRecovery

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']

@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'community']

@admin.register(Tos)
class TosAdmin(admin.ModelAdmin):
    list_display = ['version']

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['user']

@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ['title']

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ['request']

@admin.register(PasswordRecovery)
class PasswordRecoveryAdmin(admin.ModelAdmin):
    list_display = ['user']