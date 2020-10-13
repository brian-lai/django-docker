from django.apps import AppConfig


class CoreConfig(AppConfig):
    name = 'core'
    verbose_name = 'Web Core'

    def ready(self):
        # import signal handlers
        import core.signals
