import logging
import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.core.management.base import BaseCommand
from django.template.loader import render_to_string
from django_apscheduler import util
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.utils import timezone
from ...models import Post

logger = logging.getLogger(__name__)


def my_job():
    today = timezone.now()
    last_week = today - datetime.timedelta(days=7)
    #  Получаем все статьи за неделю.
    posts = Post.objects.filter(content_category='AR', date_create__gte=last_week)
    #  Получаем сет категорий, что входят в недельную рассылку.
    categories = set(posts.values_list('post_category__category_name', flat=True))
    #  Получаем сет подписчиков на эти категории.
    users = set(User.objects.filter(subscriber__category__category_name__in=categories))

    for user in users:
        #  Смотрим, на какие категории подписан конкретный пользователь.
        category_sub = user.subscriber.values_list('category__category_name', flat=True)
        #  Фильтрует статьи, которые интересуют конкретного пользователя.
        post_category_sub = set(posts.filter(post_category__category_name__in=category_sub))

        html_content = render_to_string('weekly_articles.html',
                                        {'link': f'http://127.0.0.1:8000',
                                         'posts': post_category_sub,
                                         })
        msg = EmailMultiAlternatives(
            subject='Список статей за неделю',
            body='',
            from_email='test@yandex.ru',
            to=[user.email],
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()


# The `close_old_connections` decorator ensures that database connections,
# that have become unusable or are obsolete, are closed before and after your
# job has run. You should use it to wrap any jobs that you schedule that access
# the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age`
    from the database.
    It helps to prevent the database from filling up with old historical
    records that are no longer useful.

    :param max_age: The maximum length of time to retain historical
                    job execution records. Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(day_of_week='fri', hour="18", minute="00"),
            id="my_job",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")