from core.models import CustomUser, ActivationToken, PasswordRecovery


class ProxyCustomUser(CustomUser):

    class Meta:
        proxy = True
        app_label = 'authentication'
        verbose_name = CustomUser._meta.verbose_name
        verbose_name_plural = CustomUser._meta.verbose_name_plural


class ProxyActivationToken(ActivationToken):

    class Meta:
        proxy = True
        app_label = 'authentication'
        verbose_name = ActivationToken._meta.verbose_name
        verbose_name_plural = ActivationToken._meta.verbose_name_plural


class ProxyPasswordRecovery(PasswordRecovery):

    class Meta:
        proxy = True
        app_label = 'authentication'
        verbose_name = PasswordRecovery._meta.verbose_name
        verbose_name_plural = PasswordRecovery._meta.verbose_name_plural
