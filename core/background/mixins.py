import django_rq
from django_rq.queues import get_connection

from core.background.utils import generate_object_index


class QueuedJobsMixin(object):
    def get_context_data(self, *args, **kwargs):
        context = super(QueuedJobsMixin, self).get_context_data(*args, **kwargs)

        # Add a list of job items currently active for the object
        obj = self.object
        lname = generate_object_index(obj)

        # Retrieve a list of jobs
        conn = get_connection()
        queue = django_rq.get_queue()
        context['queued_jobs'] = [queue.fetch_job(job_id) for job_id in conn.lrange(lname, 0, 10)]

        return context
