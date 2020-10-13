from django.contrib.contenttypes.models import ContentType

import django_rq
from django_rq.queues import get_connection

from core.exceptions import send_exception_email


# Instantiate logger
import logging
logger = logging.getLogger('worker')


def cleanup_task(index, job_id):
    '''Follow-up job to clean up Redis job tracker

    Args:
        index (str): Unique key where the specified job_id is located
        job_id (str): Job UUID which should be dequeued
    '''
    conn = get_connection(use_strict_redis=True)

    # Remove the first instance of the job
    conn.lrem(index, 1, job_id)
    del conn


def enqueue_task(index, func, *args, **kwargs):
    '''Adds function to RQ with tracking by index

    If index is not None, then a Redis list will manage the queued/active jobs
    related to the unique index. Jobs will be removed immediately upon completion.

    Args:
        index (str): Unique key to track queued jobs by
        func (callable): Function to be queued for background worker
        *args (list): List of parameters for func
        **kwargs (dict): Dictionary of parameters for func

    Returns:
        int: Position in queue for the given index; Defaults to None
    '''
    queue = kwargs.pop('queue', 'default')
    redis_queue = django_rq.get_queue(queue)
    # Queue the job like normal
    job = redis_queue.enqueue(func, *args, **kwargs)

    job_position = None
    # If index is None, do the queuing and return, no need to track.
    if index is not None:
        conn = get_connection(use_strict_redis=True)

        # Add the job to the list for the index
        job_position = conn.lpush(index, job.get_id())
        del conn

        # Enqueue the follow up to clean the queue when work is completed
        redis_queue.enqueue(cleanup_task, index, job.get_id(), depends_on=job)

    return job


def generate_object_index(obj):
    '''Helper method which generates a unique String for a Django models.Model instance

    Args:
        obj (:obj:`models.Model`): Django model instance

    Returns:
        str: Unique String representing `obj`
    '''
    return '%s_%s' % (
        unicode(ContentType.objects.get_for_model(obj)).lower(),
        unicode(obj.pk)
    )


def email_exception_handler(job, *exc_info):
    '''Sends an email to the admin group notifying us of a failed job.

    Additionally logs the debug trace.
    '''
    title = '%s failed' % job
    send_exception_email(
        None,
        None,
        subject=title,
        exc_info=exc_info
    )

    # Send out debug logging
    logger.debug(title, exc_info=exc_info)
