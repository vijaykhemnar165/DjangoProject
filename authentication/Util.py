from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string, get_template
from dotenv import load_dotenv
import os

load_dotenv()


class Util:
    @staticmethod
    def send_mail(data):
        """
        Static function to send email
        Args:
            data (dict): Contains email subject, email body, and email receiver.
        """
        template = get_template('invite/inviteUser.html').render(data)
        html_message_for_user = render_to_string(
            'invite/inviteUser.html', data)
        plain_message_for_user = strip_tags(html_message_for_user)
        final_message_for_user = EmailMultiAlternatives(
            data['email_subject'],
            plain_message_for_user,
            os.environ.get('EMAIL_HOST_USER'),
            [data['email_to']]
        )
        final_message_for_user.attach_alternative(template, 'text/html')
        final_message_for_user.send()
