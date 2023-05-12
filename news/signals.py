from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.template.loader import render_to_string

from NewsPaper import settings
from .models import *

# @receiver(m2m_changed, sender=Post)
# def post_created(instance, created, **kwargs):
#         if kwargs['action'] == 'post_add':
#             categories = instance.postCategory.all()
#             subscribers: list[str] = []
#             for category in categories:
#                 subscribers += category.subscribers.all()
#             subscribers = [s.email for s in subscribers]
#             send_notifications(
#                 instance.preview(),
#                 instance.pk,
#                 instance.headline,
#                 subscribers, )
#         if kwargs['action'] == 'add_post':
#             emails = User.objects.filter(
#                 subscriptions__category=instance.postCategory.all()
#             ).values_list('email', flat=True)
#
#             subject = f'Новая запись в категории {instance.category}'
#
#             text_content = (
#                 f'Тема: {instance.headline}\n'
#                 f'Превью: {instance.preview()}\n\n'
#                 f'Ссылка на публикацию: http://127.0.0.1{instance.get_absolute_url()}'
#             )
#
#             html_content = (
#                 f'Тема: {instance.headline}<br>'
#                 f'Превью: {instance.preview()}<br><br>'
#                 f'<a href="http://127.0.0.1{instance.get_absolute_url()}">'
#                 f'Ссылка на публикацию</a>'
#             )
#
#             for email in emails:
#                 msg = EmailMultiAlternatives(subject, text_content, None, [email])
#                 msg.attach_alternative(html_content, "text/html")
#                 msg.send()



def send_notifications(preview, pk, headline, subscribers):
    html_content = render_to_string(
                    'post_created_email.html',
        {
            'text': preview,
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )
    msg = EmailMultiAlternatives(
        subject=headline,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        subscribers: list[str] = []
        for category in categories:
            subscribers += category.subscribers.all()
        subscribers = [s.email for s in subscribers]
        send_notifications(
            instance.preview(),
            instance.pk,
            instance.headline,
            subscribers, )
#