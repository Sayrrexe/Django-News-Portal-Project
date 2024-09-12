from django.apps import AppConfig


class NewappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'newapp'


class SimpleappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'simpleapp'

    def ready(self):
        from . import signals