from core.admins.basic import BasicAdmin
from core.models import MeetingPoint


class MeetingPointAdmin(BasicAdmin):
    model = MeetingPoint
    list_display = ['name', 'location', 'id']
    search_fields = ['name', 'description', 'location__name']