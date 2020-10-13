import logging

from apscheduler.schedulers.blocking import BlockingScheduler
from django.conf import settings
from django.core.management.base import BaseCommand

from analysis.utils.cromwell import synchronize_cromwell_workflows
from analysis.utils.file_transfer_service import synchronize_file_transfers
from analysis.utils.workflows import build_internal_variants
from core.background.utils import enqueue_task
from core.utils.email import synchronize_mailing_lists

logger = logging.getLogger('clock')


def synchronize_mailing_list_clock():
    '''Proxy function which invokes the background work.
    '''
    # Queue background work for synchronizing `User` data.
    enqueue_task(
        'synchronize_mailing_lists',
        synchronize_mailing_lists
    )
    logger.info('Queuing mail list synchronization')


class Command(BaseCommand):
    help = 'Runs Heroku clock process'

    def handle(self, *args, **options):
        self.verbosity = options.get('verbosity')

        # Report success
        logger.info('Starting clock process')

        # Create a new `BlockingScheduler` since this is the only task to be run.
        scheduler = BlockingScheduler()

        # Email campaign lists
        scheduler.add_job(
            synchronize_mailing_list_clock,
            'cron',
            hour=settings.CLOCK_PROCESS_TIME,
            id='synchronize_mailing_list'
        )

        # Pipeline status updates
        scheduler.add_job(
            synchronize_cromwell_workflows,
            'interval',
            minutes=settings.CROMWELL_POLLING_INTERVAL,
            id='synchronize_cromwell_workflows'
        )

        # File Transfer status updates
        scheduler.add_job(
            synchronize_file_transfers,
            'interval',
            minutes=settings.FILE_TRANSFER_SERVICE_POLLING_INTERVAL,
            id='synchronize_file_transfers'
        )

        # Build internal variants database
        scheduler.add_job(
            build_internal_variants,
            'cron',
            id='build_internal_variants',
            **settings.WORKFLOW_INTERNAL_VARIANTS_SCHEDULE
        )

        scheduler.start()
