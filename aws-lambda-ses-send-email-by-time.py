import boto3
import os
from datetime import datetime

ses = boto3.client('ses')

def send_email(to_address, subject, body):
    response = ses.send_email(
        Source=os.environ['SENDER_EMAIL'],
        Destination={
            'ToAddresses': [to_address],
        },
        Message={
            'Subject': {
                'Data': subject,
            },
            'Body': {
                'Text': {
                    'Data': body,
                },
            },
        },
    )
    return response

def lambda_handler(event, context):
    # Assuming mailing lists and sender email are environment variables
    mailing_list_1 = os.environ['MAILING_LIST_1']
    mailing_list_2 = os.environ['MAILING_LIST_2']
    
    # Your email sending logic using ses.send_email()
    subject = "Your Email Subject"
    body = "Your Email Body"
    
    # Check if the current time is 3:00
    current_time = datetime.now().time()
    target_time = datetime.strptime('03:00:00', '%H:%M:%S').time()

    if current_time == target_time:
        # Send email to the first mailing list
        response = send_email(mailing_list_1, subject, body)
    else:
        # Send email to the second mailing list
        response = send_email(mailing_list_2, subject, body)

    return {
        'statusCode': 200,
        'body': f'Email sent successfully! MessageId: {response["MessageId"]}'
    }
