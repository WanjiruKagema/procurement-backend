from django.conf import settings
from django.core import mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


class Mailer:
    """
    Send email messages helper class
    """

    def __init__(self):
        # TODO setup the default from email
        self.connection = mail.get_connection()
        self.from_email = settings.EMAIL_HOST_USER

    def send_messages(self, subject, context, form_description, form_status):
        messages = self.__generate_messages(subject, context, form_description, form_status)
        self.__send_mail(messages)

    def __send_mail(self, mail_messages):
        self.connection.open()
        self.connection.send_messages(mail_messages)
        self.connection.close()

    def __generate_messages(self, subject, context, form_description, form_status):

        messages = []

        for recipient in context:
            template = render_to_string(
                'emails/procurementplan_status.html',
                {'name': recipient['name'],
                 'proc_description': form_description,
                 'proc_status': form_status,
                 })

            message = EmailMessage(subject, template, to=[recipient['email']], from_email=self.from_email)
            # message.content_subtype = 'html'
            messages.append(message)

        return messages
