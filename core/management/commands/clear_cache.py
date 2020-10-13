import logging

from django.core.cache import cache
from django.core.management.base import BaseCommand

logger = logging.getLogger('management')


class Command(BaseCommand):
    help = 'Clears the application cache'

    def handle(self, *args, **options):
        self.verbosity = options.get('verbosity')

        # Call to invalidate the entire cache
        cache.clear()

        # Report success
        if self.verbosity > 0:
            logger.info('Cleared application cache.')
