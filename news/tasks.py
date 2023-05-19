from celery import shared_task, app
import time
from django.template.loader import render_to_string
from NewsPaper import settings
from django.core.mail import EmailMultiAlternatives
from .models import *
from datetime import datetime, timedelta

import logging
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model


@shared_task
def hello():
    time.sleep(10)
    print("Hello! I left this message for check of working celery")


@shared_task
def printer(N):
    for i in range(N):
        time.sleep(1)
        print(i+1)


@shared_task
def send_notify(instance_id):
    instance = Post.objects.get(pk=instance_id)
    categories = instance.postCategory.all()
    subscribers = []
    for category in categories:
        subscribers += category.subscribers.all()
    subscribers = list(set(s.email for s in subscribers))
    print(subscribers)

    for mail in subscribers:
        html_content = render_to_string(
            'post_created_email.html',
            {
                'text': instance.preview,
                'link': f'{settings.SITE_URL}/news/{instance_id}',
            }
        )
        msg = EmailMultiAlternatives(
            subject=instance.headline,
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[mail],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()


@shared_task
def week_notify():
    today = datetime.now()
    last_week = today - timedelta(days=7)
    posts = Post.objects.filter(pubDate__gte=last_week)
    categories = set(posts.values_list('postCategory__catName', flat=True))
    subscribers = set(Category.objects.filter(catName__in=categories).values_list('subscribers__email', flat=True))
    html_content = render_to_string(
        'post_created_email.html',
        {
            'link': settings.SITE_URL,
            'posts': posts,
        }
    )
    msg = EmailMultiAlternatives(
        subject='Недельные новости',
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers,
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()