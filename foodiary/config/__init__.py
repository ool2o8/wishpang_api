from django.apps import AppConfig
from . import settings


class SubscriptionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'subscription'

    def ready(self, request):
        if settings.SCHEDULER_DEFAULT:
            from . import operator
            operator.start(request)