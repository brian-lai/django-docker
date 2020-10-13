from django.test import TestCase

from django_hosts import resolvers


# Resolvers are a wonderful thing when they work
# This kind of test allows name chaning to happen, but will catch when a signature no longer matches
class URLTestCases(TestCase):
    # SUBJECT
    def test_auditview(self):
        resolvers.reverse('history', host='dashboard', kwargs={'content_type': 1, 'object_id': 1})
        self.assertTrue(True)

    def test_scanmodalview(self):
        resolvers.reverse('scanner_modal', host='dashboard')
        self.assertTrue(True)
