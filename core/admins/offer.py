from django.contrib import admin
from django.contrib.auth.models import User
from django.forms import BaseInlineFormSet
from core.admins.basic import BasicAdmin
from core.models import Message, Meeting, Evaluation, Offer


class UserBasedFormset(BaseInlineFormSet):

    def add_fields(self, form, index):
        super(UserBasedFormset, self).add_fields(form, index)
        form.fields['user'].queryset = User.objects.all()
        try:
            if form.fields['offer'].parent_instance:
                parent = form.fields['offer'].parent_instance
                ids = [parent.user.pk, parent.request.user.pk]
                form.fields['user'].queryset = User.objects.filter(id__in=ids)
        except:
            pass


class MessageInline(admin.TabularInline):
    model = Message
    formset = UserBasedFormset
    extra = 1


class MeetingInline(admin.TabularInline):
    model = Meeting
    formset = UserBasedFormset
    extra = 1


class EvaluationInline(admin.TabularInline):
    model = Evaluation
    max_num = 2
    extra = 1


class OfferAdmin(BasicAdmin):
    model = Offer
    list_display = ['user', 'request', 'closed', 'id', 'is_evaluated']
    search_fields = ['user__username', 'request__title', 'detail']
    list_filter = ['closed']
    inlines = [MessageInline, MeetingInline, EvaluationInline]