from api.mail_templates.message import new_message_notification_message
from api.mail_templates.offer import new_offer_notification_message
from api.mail_templates.meeting import new_meeting_notification_message
from api.utils.asyncronous_mail import send_mail
from core.models import Profile
from core.models.notification import Notification


class Notifier():
    """ """

    @staticmethod
    def notify(photo, user, title, message, link, mail_subject, mail_body):
        """
        Create Notification object
        Send mail
        """
        profile = Profile.objects.get(user=user)
        n = Notification(photo=photo,
                         user=user,
                         title=title,
                         message=message,
                         link=link)
        n.save()
        if not profile.mail_notification:
            return
        send_mail(subject=mail_subject,
                  body=mail_body,
                  from_email='notifications@smartribe.fr',
                  recipient_list=[user.email],
                  fail_silently=False)

    @staticmethod
    def notify_new_offer(offer):
        """ """
        user = offer.request.user
        profile = Profile.objects.get(user=user)
        s, b = new_offer_notification_message(offer)
        if not profile.mail_notification:
            return
        Notifier.notify(photo=offer.user.profile.photo,
                        user=user,
                        title=offer.request.title,
                        message='Nouvelle proposition de %s %s' % (offer.user.first_name, offer.user.last_name),
                        link='/offers/' + str(offer.id) + '/',
                        mail_subject=s,
                        mail_body=b)

    @staticmethod
    def notify_new_message(message):
        """ """
        author = message.user
        if message.user.id == message.offer.user.id:
            user = message.offer.request.user
        else:
            user = message.offer.user
        s, b = new_message_notification_message(message, message.user, user)
        Notifier.notify(photo=author.profile.photo,
                        user=user,
                        title=message.offer.request.title,
                        message='Nouveau message de %s %s' % (message.user.first_name, message.user.last_name),
                        link='/offers/' + str(message.offer.id) + '/',
                        mail_subject=s,
                        mail_body=b)

    @staticmethod
    def notify_new_meeting(meeting):
        """ """
        author = meeting.user
        if meeting.user.id == meeting.offer.user.id:
            user = meeting.offer.request.user
        else:
            user = meeting.offer.user
        s, b = new_meeting_notification_message(meeting, meeting.user, user)
        Notifier.notify(photo=author.profile.photo,
                        user=user,
                        title=meeting.offer.request.title,
                        message='Nouveau rendez-vous proposé par %s %s' % (meeting.user.first_name, meeting.user.last_name),
                        link='/offers/' + str(meeting.offer.id) + '/',
                        mail_subject=s,
                        mail_body=b)
