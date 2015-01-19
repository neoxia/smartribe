from django.contrib import admin
from core.admins.basic import BasicAdmin
from core.models import MeetingPoint, Location


class MeetingPointInline(admin.TabularInline):
    model = MeetingPoint
    extra = 1


class LocationAdmin(BasicAdmin):
    model = Location
    list_display = ['name', 'community', 'index', 'id']
    search_fields = ['community__name', 'name', 'description']
    inlines = [MeetingPointInline]