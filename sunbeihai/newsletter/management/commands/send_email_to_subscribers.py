#!/usr/bin/env python
"""To send emails to subscribers."""
from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail
from django.conf import settings
from newsletter.models import Newsletter
from course.models import Subscriber

class Command(BaseCommand):

    help = "Send email newsletter to subscribers"

    def handle(self, *args, **options):
        # Get a list of subscribers
        subscribers = Subscriber.objects.all()
        
        # Get the latest newsletter
        newsletter = Newsletter.objects.latest('published_at')
        
        newsletter_content = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Newsletter from Sun Beihai</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">
            </head>
            <body>
                <div class="container">
                    <p>Welcome to <a href="https://www.sunbeihai.com/">sunbeihai.com</a>!</p>
                </div>
            </body>
            </html>
            """
        
        with open(newsletter.file.path, 'rb') as f:
            newsletter_content = f.read().decode('utf-8')
    
        # Loop over each subscriber and send the newsletter
        self.stdout.write("Starting to send newsletters ...", ending="\n")
        
        for s in subscribers:
            subject = newsletter.subject
            send_mail(
                subject, 
                '', 
                settings.EMAIL_HOST_USER, 
                [s.email], 
                html_message=newsletter_content, 
                fail_silently=False)
            
            self.stdout.write(self.style.SUCCESS(f'\tNewsletter sent to {s.email}'))
    
        # Finish sending the newsletter all subscribers.
        self.stdout.write(self.style.SUCCESS(f'Newsletter sent to {len(subscribers)} subscribers.'))