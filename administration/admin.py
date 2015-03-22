from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import Permission
from administration.models import ProxySuggestion, ProxyInappropriate, ProxyFaqSection, ProxyTos, ProxyFaq


class SuggestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'category', 'user_link', 'title']
    list_filter = ['category']
    search_fields = ['user__last_name', 'user__first_name', 'user__email', 'title']

    def user_link(self, item):
        return '<a href="../../authentication/proxycustomuser/%d/">%s</a>' % (item.user.id, str(item.user))
    user_link.allow_tags = True


class InappropriateAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_link', 'content_identifier']
    search_fields = ['user__last_name', 'user__first_name', 'user__email', 'content_identifier']

    def user_link(self, item):
        return '<a href="../../authentication/proxycustomuser/%d/">%s</a>' % (item.user.id, str(item.user))
    user_link.allow_tags = True


class FaqSectionAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']


class FaqAdmin(admin.ModelAdmin):
    list_display = ['id', 'section_link', 'question', 'private']
    list_filter = ['section', 'private']
    search_fields = ['question', 'answer']

    def section_link(self, item):
        return '<a href="../../administration/proxyfaqsection/%d/">%s</a>' % (item.section.id, str(item.section))
    section_link.allow_tags = True


admin.site.register(LogEntry)
admin.site.register(Permission)
admin.site.register(ProxyTos)
admin.site.register(ProxyFaqSection, FaqSectionAdmin)
admin.site.register(ProxyFaq, FaqAdmin)
admin.site.register(ProxyInappropriate, InappropriateAdmin)
admin.site.register(ProxySuggestion, SuggestionAdmin)