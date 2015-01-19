from core.admins.basic import BasicAdmin
from core.models import Message


class MessageAdmin(BasicAdmin):
    model = Message
    list_display = ['user', 'offer', 'creation_date', 'id']
    search_fields = ['user__username', 'content']
    list_filter = ['creation_date']