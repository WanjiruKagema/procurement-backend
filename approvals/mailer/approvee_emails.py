from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def procurement_approve_email(approvee_name, proc_description, date, approvee_comment, proc_status, approvee_email):
    template = render_to_string(
        'emails/approvee.html',
        {'name': approvee_name,
         'proc_description': proc_description,
         'proc_status': proc_status,
         'date': date,
         'comment': approvee_comment
         })
    email = EmailMessage(
        f'ProcurementPlan Approval Status Recorded',
        template,
        settings.EMAIL_HOST_USER,
        [approvee_email],
    )
    email.fail_silently = True

    return email



