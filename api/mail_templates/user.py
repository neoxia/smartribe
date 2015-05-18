from django.conf import settings


def registration_message(activation_token):
    s = '[SmarTribe] Registration confirmation'
    m = 'Cher '+ activation_token.user.first_name +', \n\n' \
        'Vous venez de vous inscrire sur SmarTribe et nous vous en remercions.\n\n' \
        'Afin de confirmer votre inscription, merci de suivre le lien suivant: \n\n' \
        'https://smartribe.fr/#/user/' + activation_token.token + '/activation \n\n' \
        'Cordialement.\n\n' \
        'L\'équipe SmarTribe'
    return s, m


def recovery_password_message(recovery_token):
    s = '[SmarTribe] Password recovery'
    m = 'Cher '+ recovery_token.user.first_name +', \n\n' \
        'Vous avez demandé à réinitialiser votre mot de passe. Votre demande à été prise en compte.\n' \
        'Vous disposez dès lors de ' + str(settings.PRT_VALIDITY) + ' heure pour vous connecter au site ' \
        'à l\'adresse suivante : \n\n' \
        'https://smartribe.fr/#/password/' + recovery_token.token + '/edit \n\n' \
        'Si vous n\'avez pas pu effectuer cette opération dans ce délai, merci de renouveler votre' \
        'demande.\n\n' \
        'Cordialement.\n\n' \
        'L\'équipe SmarTribe'
    return s, m
