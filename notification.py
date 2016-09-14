#
#  ______________________
# / Simple Notifications \
# \ By Davide Nastri     /
#  ----------------------
#     \ ^__^
#      \(oo)\_______
#       (__)\       )\/\
#         ||-----w |
#         ||      ||
#
# This script sends notification using
# Email, Pushbullet or Pushover
#
# Please put your data into configure.py before using this script

import configuration
import requests
import json
import smtplib
import sys
import httplib, urllib
from email.mime.text import MIMEText

server = smtplib.SMTP()

def send_email(email_subject, notification_msg, email_recipients):
    '''
    This functions sends a notification using Email
            Args:
            email_subject (str) : Email Subject.
            notification_msg (str) : Email Body.
            email_recipients (str) : Email recipients.
    '''
    server.connect(configuration.EMAIL_SERVER, configuration.EMAIL_SERVER_PORT)
    if configuration.EMAIL_DEBUG_LEVEL == '1':
        server.set_debuglevel(1)
    recipients = [email_recipients]
    msg = MIMEText(notification_msg)
    msg['Subject'] = email_subject
    msg['From'] = configuration.EMAIL_SENDER
    msg['To'] = ', '.join(recipients)
    server.ehlo()
    server.starttls()
    server.ehlo
    server.login(configuration.EMAIL_SENDER, configuration.EMAIL_PASSWORD)
    server.sendmail(configuration.EMAIL_SENDER, recipients, msg.as_string())
    server.quit()


def send_pushover_notification(body):
    '''
    This functions sends a notification using Pushover
        Args:
            body (str) : Body of text.
    '''
    conn = httplib.HTTPSConnection("api.pushover.net")
    conn.request("POST", "/1/messages.json",
      urllib.urlencode({
        "token": configuration.PUSHOVER_APP_TOKEN,
        "user": configuration.USER_KEY,
        "message": body,
      }), { "Content-type": "application/x-www-form-urlencoded" })
    response = conn.getresponse()
    if response.status != 200:
        raise Exception('Something wrong')
    else:
        print 'Sending complete'


def send_pushbullet_notification(title, body):
    '''
    This function sends a notification using Pushbullet
        Args:
            title (str) : title of text.
            body (str) : Body of text.
    '''
    data_send = {"type": "note", "title": title, "body": body}
    resp = requests.post('https://api.pushbullet.com/v2/pushes', data=json.dumps(data_send),
                         headers={'Authorization': 'Bearer ' + configuration.PUSHBULLET_APP_TOKEN, 'Content-Type': 'application/json'})
    if resp.status_code != 200:
        raise Exception('Something wrong')
    else:
        print 'Sending complete'


def display_help():
    '''
    This functions displays the command help
    '''
    print 'Email     Example: --email "Email Subject" "Email Message" "Email recipients"'
    print 'Pusbullet Example: --pushbullet "Title" "Message"'
    print 'Pushover  Example: --pushover "Message"'


def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "--email":
            print len(sys.argv)
            if len(sys.argv) == 5:
                EMAIL_SUBJECT = sys.argv[2]
                EMAIL_MESSAGE = sys.argv[3]
                EMAIL_RECIPIENTS = sys.argv[4]
                send_email(EMAIL_SUBJECT, EMAIL_MESSAGE, EMAIL_RECIPIENTS)
            else:
                display_help()
        elif sys.argv[1] == "--pushover":
            if len(sys.argv) == 3:
                send_pushover_notification(sys.argv[2])
            else:
                display_help()
        elif sys.argv[1] == "--pushbullet":
            if len(sys.argv) == 4:
                send_pushbullet_notification(sys.argv[2], sys.argv[3])
            else:
                display_help()
        else:
            display_help()
    else:
        display_help()


if __name__ == '__main__':
    main()
