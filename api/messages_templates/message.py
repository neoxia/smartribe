

def new_message_notification_message(message):
    s = '[SmarTribe] Nouveau message'
    m = 'Cher '+ message.offer.request.user.username +', \n\n' \
        'Vous avez reçu un nouveau message concernant votre demande :\n\n' \
        '\t ' + message.offer.request.title + '\n\n' \
        'Vous pouvez le consulter en vous connectant à votre espace personnel sur www.smartribe.fr \n\n' \
        'Cordialement.\n\n' \
        'L\'équipe SmarTribe'
    return s, m
