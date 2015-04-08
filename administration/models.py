from core.models import Tos, Suggestion, FaqSection, Faq, Inappropriate
from core.models.text import Text


class ProxyTos(Tos):

    class Meta:
        proxy = True
        app_label = 'administration'
        verbose_name = Tos._meta.verbose_name
        verbose_name_plural = Tos._meta.verbose_name_plural


class ProxySuggestion(Suggestion):

    class Meta:
        proxy = True
        app_label = 'administration'
        verbose_name = Suggestion._meta.verbose_name
        verbose_name_plural = Suggestion._meta.verbose_name_plural


class ProxyFaqSection(FaqSection):

    class Meta:
        proxy = True
        app_label = 'administration'
        verbose_name = FaqSection._meta.verbose_name
        verbose_name_plural = FaqSection._meta.verbose_name_plural


class ProxyFaq(Faq):

    class Meta:
        proxy = True
        app_label = 'administration'
        verbose_name = Faq._meta.verbose_name
        verbose_name_plural = Faq._meta.verbose_name_plural


class ProxyInappropriate(Inappropriate):

    class Meta:
        proxy = True
        app_label = 'administration'
        verbose_name = Inappropriate._meta.verbose_name
        verbose_name_plural = Inappropriate._meta.verbose_name_plural


class ProxyText(Text):

    class Meta:
        proxy = True
        app_label = 'administration'
        verbose_name = Text._meta.verbose_name
        verbose_name_plural = Text._meta.verbose_name_plural
