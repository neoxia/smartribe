from django.contrib import admin
from authentication.models import ProxyCustomUser, ProxyPasswordRecovery, ProxyActivationToken
from core.admins.basic import BasicAdmin
from core.admins.custom_user import CustomUserAdmin


class ActivationTokenAdmin(BasicAdmin):
    list_display = ['id', 'user']


admin.site.register(ProxyCustomUser, CustomUserAdmin)
admin.site.register(ProxyActivationToken, ActivationTokenAdmin)
admin.site.register(ProxyPasswordRecovery, ActivationTokenAdmin)
