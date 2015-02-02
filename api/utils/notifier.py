from email import message
from api.messages_templates.message import new_message_notification_message
from api.messages_templates.offer import new_offer_notification_message
from api.utils.asyncronous_mail import send_mail
from core.models.notification import Notification


class Notifier():
    """ """

    @staticmethod
    def notify(user, message, link, mail_subject, mail_body):
        """
        Create Notification object
        Send mail
        """
        n = Notification(user=user,
                         message=message,
                         link=link)
        n.save()
        send_mail(subject=mail_subject,
                  body=mail_body,
                  from_email='notifications@smartribe.fr',
                  recipient_list=[user.email],
                  fail_silently=False)

    @staticmethod
    def notify_new_offer(offer):
        """ """
        user = offer.request.user
        s, b = new_offer_notification_message(offer)
        Notifier.notify(user=user,
                        message='Nouvelle proposition d\'assistance',
                        link='offers/' + str(offer.id) + '/',
                        mail_subject=s,
                        mail_body=b)



    @staticmethod
    def notify_new_message(message):
        """ """
        if message.user == message.offer.user:
            user = message.offer.request.user
        else:
            user = message.offer.user
        s, b = new_message_notification_message(message)
        Notifier.notify(user=user,
                        message='Nouveau message',
                        link='messages/' + str(message.id) + '/',
                        mail_subject=s,
                        mail_body=b)
