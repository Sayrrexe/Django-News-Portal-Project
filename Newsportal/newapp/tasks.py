from celery import shared_task
from django.core.mail import EmailMultiAlternatives
import time

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import Subscription, Post
from datetime import datetime, timedelta

# Функция отправки уведомления автору о создании новой статьи
@shared_task
def new_post_notification(subj, email, content):
    time.sleep(5)

    msg = EmailMultiAlternatives(
        subject=subj,
        body='',
        from_email='pyataevfamily@yandex.ru',
        to=[email],
    )
    msg.attach_alternative(content, "text/html")
    msg.send()


# Еженедельная рассылка новых новостей
@shared_task()
def weekly_notification():
    print("----------------------------------------------------------------------------------------------------------------------")
    if Subscription.objects.all().exists():
        subscribers = Subscription.objects.all()
        for subscriber in subscribers:
            user = subscriber.id_user
            print(user)
            subject = f'Здравствуй, {user}! Еженедельная рассылка новостей по категории "{subscriber.id_category}"'

            postList = Post.objects.filter(created__gte=(datetime.today() - timedelta(days=7)), id_post_category=subscriber.id_category.pk)
            for post in postList:
                print(post.header, post.created, subscriber.id_category)

            html_content = render_to_string('distribution.html', {'postList': postList, })
            msg = EmailMultiAlternatives(
                subject=subject,
                body='',
                from_email='pyataevfamily@yandex.ru',
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()