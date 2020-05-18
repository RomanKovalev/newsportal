from celery.decorators import task
from celery.utils.log import get_task_logger
from django.core.mail import EmailMessage


logger = get_task_logger(__name__)


@task(name="send_email_task")
def send_email_task(mail_subject, message, to_email):
    email = EmailMessage(mail_subject, message, to=[to_email])
    return email.send()