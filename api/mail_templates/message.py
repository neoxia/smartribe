

def new_message_notification_message(message, sender, recipient):
    s = '[SmarTribe] Nouveau message'
    m = 'Cher '+ recipient.username +', \n\n' \
        'Vous avez reçu un nouveau message de ' + sender.username + '\n\n' \
        'Vous pouvez le consulter en vous connectant à votre espace personnel sur www.smartribe.fr \n\n' \
        'Cordialement.\n\n' \
        'L\'équipe SmarTribe'
    return s, m
