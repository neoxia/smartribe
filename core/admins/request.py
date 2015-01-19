from django.contrib import admin
from core.admins.basic import BasicAdmin
from core.models import Offer, Request


class OfferInline(admin.TabularInline):
    model = Offer
    extra = 1


class RequestAdmin(BasicAdmin):
    model = Request
    list_display = ['user', 'category', 'title', 'community', 'closed', 'id', 'get_offers_count']
    search_fields = ['user__username', 'category__name', 'title', 'community__name']
    list_filter = ['category', 'closed']
    inlines = [OfferInline]