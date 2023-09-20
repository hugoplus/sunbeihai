import base64
from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email_async(subject, message, from_email, recipient_list):
    try:
        send_mail(
            subject=subject, 
            message="Please enable HTML in your email client to view this message.", 
            from_email=from_email, 
            recipient_list=recipient_list, 
            html_message=message
        )
        return True  # Email sent successfully
    except Exception as e:
        print(f"Email sending failed: {str(e)}")
        return False  # Email sending failed