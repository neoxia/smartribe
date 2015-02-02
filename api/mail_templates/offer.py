

def new_offer_notification_message(offer):
    s = '[SmarTribe] Nouvelle proposition'
    m = 'Cher '+ offer.request.user.username +', \n\n' \
        'Vous avez reçu une nouvelle proposition d\'aide concernant votre demande :\n\n' \
        '\t ' + offer.request.title + '\n\n' \
        'Vous pouvez la consulter en vous connectant à votre espace personnel sur www.smartribe.fr \n\n' \
        'Cordialement.\n\n' \
        'L\'équipe SmarTribe'
    return s, m
