from django.contrib import admin
from django.contrib.admin.models import LogEntry
from administration.models import ProxySuggestion, ProxyInappropriate, ProxyFaqSection, ProxyTos, ProxyFaq


admin.site.register(LogEntry)
admin.site.register(ProxyTos)
admin.site.register(ProxyFaqSection)
admin.site.register(ProxyFaq)
admin.site.register(ProxyInappropriate)
admin.site.register(ProxySuggestion)