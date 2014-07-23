from django.contrib import admin
from core.models import Member
from core.models.activation_token import ActivationToken
from core.models.address import Address
from core.models.skill import SkillCategory
from .models import Profile
from .models import User
from .models import Community
from .models import TransportCommunity
from .models import LocalCommunity
from .models import TransportStop
from .models import Tos
from .models import Skill
from .models import Request
from .models import Offer
from .models import PasswordRecovery


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email']


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(TransportCommunity)
class TransportCommunityAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(LocalCommunity)
class LocalCommunityAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(TransportStop)
class TransportStopAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'community']


@admin.register(Tos)
class TosAdmin(admin.ModelAdmin):
    list_display = ['version']


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']


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


@admin.register(ActivationToken)
class ActivationTokenAdmin(admin.ModelAdmin):
    list_display = ['user']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['city']
