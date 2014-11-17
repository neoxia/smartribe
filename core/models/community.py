from django.db import models
from core.models import Address
from core.models.validator import ZipCodeValidatorFR


def get_banner_path(self, filename):
    url = "communities/%s/banner/%s" % (self.name, filename)
    return url


def get_logo_path(self, filename):
    url = "communities/%s/logo/%s" % (self.name, filename)
    return url


class Community(models.Model):

    name = models.CharField(max_length=50, unique=True)

    description = models.TextField(max_length=180)

    banner = models.ImageField(upload_to=get_banner_path,
                               blank=True, null=True)

    logo = models.ImageField(upload_to=get_logo_path,
                             blank=True, null=True)

    creation_date = models.DateField(auto_now_add=True)

    last_update = models.DateField(auto_now=True)

    auto_accept_member = models.BooleanField(default=False)

    def get_type(self):
        """
        Returns the type of the community as a capital letter.
        """
        try:
            self.localcommunity
            return "L"
        except LocalCommunity.DoesNotExist:
            pass
        try:
            self.transportcommunity
            return "T"
        except TransportCommunity.DoesNotExist:
            pass
        return "O"

    def get_members_count(self):
        from core.models.member import Member
        return Member.objects.filter(community=self).count()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'community'
        verbose_name_plural = 'communities'
        app_label = 'core'


class TransportCommunity(Community):

    departure = models.CharField(max_length=255)

    via = models.CharField(max_length=255,
                           null=True, blank=True)

    arrival = models.CharField(max_length=255)

    def __str__(self):
        return self.name+', de '+self.departure \
            + ' à '+self.arrival \
            + ', via '+self.via

    class Meta:
        verbose_name = 'transport community'
        verbose_name_plural = 'transport communities'
        app_label = 'core'


class LocalCommunity(Community):

    gps_x = models.FloatField()

    gps_y = models.FloatField()

    street_num = models.IntegerField(blank=True, null=True)

    street = models.CharField(max_length=100,
                              blank=True, null=True)

    zip_code = models.CharField(max_length=10,
                                blank=True, null=True,
                                validators=[ZipCodeValidatorFR(), ])

    city = models.CharField(max_length=100)

    country = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'local community'
        verbose_name_plural = 'local communities'
        app_label = 'core'
