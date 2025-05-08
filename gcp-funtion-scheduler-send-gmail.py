import os
import base64
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from google.oauth2 import service_account
from email.mime.text import MIMEText

def send_email(to_emails, subject, body):
    credentials = service_account.Credentials.from_service_account_file(
        'credentials.json',
        scopes=['https://www.googleapis.com/auth/gmail.send'],
    )
    service = build('gmail', 'v1', credentials=credentials)

    message = MIMEText(body)
    message['to'] = ', '.join(to_emails)
    message['from'] = os.environ['SENDER_EMAIL']
    message['subject'] = subject

    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    create_message = {'raw': encoded_message}

    send_result = service.users().messages().send(userId='me', body=create_message).execute()
    return send_result

def send_scheduled_email(request):
    now = datetime.now()
    target = now.replace(hour=3, minute=0, second=0, microsecond=0)
    window_end = target + timedelta(minutes=1)

    mailing_list_1 = os.environ.get('MAILING_LIST_1', '').split(',')
    mailing_list_2 = os.environ.get('MAILING_LIST_2', '').split(',')

    subject = "Your Email Subject"
    body = "Your Email Body"

    try:
        if target <= now < window_end:
            result = send_email(mailing_list_1, subject, body)
        else:
            result = send_email(mailing_list_2, subject, body)

        return {"status": "success", "messageId": result.get("id")}
    except Exception as e:
        return {"status": "error", "message": str(e)}
