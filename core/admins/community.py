from django.contrib import admin
from core.admins.basic import BasicAdmin
from core.models import Member, Location, Community, LocalCommunity, TransportCommunity


class MemberInline(admin.TabularInline):
    model = Member
    extra = 1


class LocationInline(admin.TabularInline):
    model = Location
    extra = 1


class CommunityAdmin(BasicAdmin):
    model = Community
    list_display = ['name', 'get_members_count', 'get_type', 'id']
    search_fields = ('name', 'description')
    inlines = [MemberInline, LocationInline]


class LocalCommunityAdmin(CommunityAdmin):
    model = LocalCommunity
    list_display = ['name', 'zip_code', 'city', 'id', 'get_members_count']
    search_fields = ['name', 'description', 'street', 'city', 'zip_code']


class TransportCommunityAdmin(CommunityAdmin):
    model = TransportCommunity
    list_display = ['name', 'departure', 'via', 'arrival', 'id', 'get_members_count']
    search_fields = ['name', 'description', 'departure', 'via', 'arrival']