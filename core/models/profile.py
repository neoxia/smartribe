import os
from django.db.models import Q
from django.utils.translation import ugettext as _
from django.conf import settings
from django.db import models
import math
from core.models.skill import Skill
from core.models.meeting import Meeting
from core.models.offer import Offer
from core.models.request import Request
from core.models.member import Member
from core.models.evaluation import Evaluation
from core.models.message import Message
from core.models.donation import Donation
from core.models.validator import PhoneValidatorFR, ZipCodeValidatorFR


def get_photo_path(self, filename):
    _, ext = os.path.splitext(filename)
    url = "profiles/%s/picture%s" % (str(self.user.id), ext)
    return url

#fs = FileSystemStorage(location='/media/photos')


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')

    GENDER_CHOICES = (
                     ('M', _('Male')),
                     ('F', _('Female')),
                     ('O', _('Other')),
    )
    gender = models.CharField(max_length=2,
                              choices=GENDER_CHOICES,
                              default='O')

    street_num = models.IntegerField(blank=True, null=True)

    street = models.CharField(max_length=100,
                              blank=True, null=True)

    zip_code = models.CharField(max_length=10,
                                blank=True, null=True,
                                validators=[ZipCodeValidatorFR(), ])

    city = models.CharField(max_length=100,
                            blank=True, null=True)

    country = models.CharField(max_length=50,
                               blank=True, null=True)

    phone = models.CharField(max_length=15,
                             validators=[PhoneValidatorFR(), ],
                             blank=True,
                             null=True)

    birthdate = models.DateField(blank=True,
                                 null=True)

    bio = models.TextField(blank=True,
                           null=True)

    photo = models.ImageField(upload_to=get_photo_path,
                              #storage=fs,
                              blank=True,
                              null=True)

    mail_notification = models.BooleanField(default=True)

    CONTACT_CHOICES = (
        ('E', _('Email')),
        ('P', _('Phone')),
        ('N', _('None')))
    favorite_contact = models.CharField(max_length=2,
                                        choices=CONTACT_CHOICES,
                                        default='N')

    @property
    def is_early_adopter(self):
        return self.user.id <= settings.EARLY_ADOPTER_MAX_ID

    def early_adopter(self):
        return self.is_early_adopter
    early_adopter.boolean = True
    early_adopter.allow_tags = True

    @property
    def is_donor(self):
        return Donation.objects.filter(user=self.user).exists()

    def donor(self):
        return self.is_donor
    donor.boolean = True
    donor.allow_tags = True

    def get_skills(self):
        # TODO : Test
        from core.models.skill import Skill
        return Skill.objects.filter(user=self.user)

    def get_user_level(self):
        # Profile level [1]
        # (Profile completion [0.6] + skills [0.4])
        skills = self.get_skills_count() * 0.15
        profile_level = self.get_profile_completion() * 0.6 + self.get_value(skills, 0.4)

        # Requests level [0.5]
        # (0.1 / request)
        requests = self.get_requests_count() * 0.1
        request_level = self.get_value(requests, 0.5)

        # Offers Level [1]
        # (0.1 / offer)
        offers_max = 1.5 - request_level
        offers = self.get_requests_count() * 0.1
        offer_level = self.get_value(offers, offers_max)

        # Messages level [0.5]
        # (0.01 / message)
        messages = self.get_messages_count() * 0.01
        message_level = self.get_value(messages, 0.5)

        # Meetings level [0.5]
        # (0.2 / meeting)
        meetings = self.get_meetings_count() * 0.2
        meeting_level = self.get_value(meetings, 0.5)

        # Evaluations given level [0.5]
        # (0.05 / evaluation)
        evaluations_g = self.get_evaluations_by_me_count() * 0.05
        evaluation_g_level = self.get_value(evaluations_g, 0.5)

        # Evaluations received level [1]
        # (0.05 / evaluation)
        evaluations_r = self.get_evaluations_for_me_count() * 0.05
        evaluation_r_level = self.get_value(evaluations_r, 0.5)

        # TOTAL [5]
        total =  profile_level + request_level + offer_level + message_level + meeting_level \
               + evaluation_g_level + evaluation_r_level
        return round(total, 2)

    get_user_level.allow_tags = True

    def get_value(self, value, max):
        return value if value <= max else max

    def get_title(self):
        rank = math.floor(self.get_user_level())
        return settings.XP_TITLE_CHOICES[rank]
    get_title.allow_tags = True

    def get_profile_completion(self):
        """ Including skills """
        excluded = ['id', 'user', 'gender', 'mail_notification', 'favorite_contact']
        i = 0
        sum = 0
        for field in Profile._meta.get_all_field_names():
            if field in excluded:
                continue
            i += 1
            sum += 1 if getattr(self, field) else 0
        return round(sum / i, 2)
    get_profile_completion.allow_tags = True

    def get_skills_count(self):
        return Skill.objects.filter(user=self.user).count()

    def get_memberships_count(self):
        return Member.objects.filter(user=self.user, status="1").count()

    def get_requests_count(self):
        return Request.objects.filter(user=self.user).count()

    def get_offers_count(self):
        return Offer.objects.filter(user=self.user).count()

    def get_messages_count(self):
        return Message.objects.filter(user=self.user).count()

    def get_meetings_count(self):
        return Meeting.objects.filter(Q(offer__user=self.user) | Q(offer__request__user=self.user)).count()

    def get_evaluations_for_me_count(self):
        return Evaluation.objects.filter(offer__user=self.user).count()

    def get_evaluations_by_me_count(self):
        return Evaluation.objects.filter(offer__request__user=self.user).count()

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = _('profile')
        verbose_name_plural = _('profiles')
        app_label = 'core'


