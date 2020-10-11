from django.core.mail import send_mail

def send_notif():
    send_mail(
        'Subject Here',
        'Here is the message',
        'ipsit.iitb@gmail.com',
        ['webnominee.iitb@gmail.com']
    )



def my_cron_job():
    print('I will be printed every 1 min')
    return True