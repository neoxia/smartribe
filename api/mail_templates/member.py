def new_member_notification_message(community, sender, recipient):
    s = '[SmarTribe] Nouveau membre'
    if community.auto_accept_member:
        m = 'Cher '+ recipient.first_name +', \n\n' \
            + sender.first_name + ' ' + sender.last_name + ' fait désormais partie de votre communauté "' \
            + community.name + '".\n\n' \
            'Vous pouvez gérer ses membres en vous connectant à votre espace personnel sur www.smartribe.fr \n\n' \
            'Cordialement.\n\n' \
            'L\'équipe SmarTribe'
    else:
        m = 'Cher '+ recipient.first_name +', \n\n' \
            + sender.first_name + ' ' + sender.last_name + ' demande à faire partie de votre communauté "' \
            + community.name + '".\n\n' \
            'Vous pouvez valider sa demande en vous connectant à votre espace personnel sur www.smartribe.fr \n\n' \
            'Cordialement.\n\n' \
            'L\'équipe SmarTribe'
    return s, m