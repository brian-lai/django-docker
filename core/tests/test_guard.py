from django.contrib.auth.models import Group, User
from django.test import TestCase

from core.guard.shortcuts import assign_creator
from gist.models import Package


class GuardTestCases(TestCase):
    fixtures = ['users.json', 'groups.json', 'users_profile_settings.json', 'groups_gistprofile.json']

    def setUp(self):
        self.genepeeks = Group.objects.get(pk=1)
        self.admin = User.objects.get(pk=1)
        self.lab = Group.objects.get(pk=3)

    # Tests `core.guard.signals._handle_post_save`
    def test_creator(self):
        package = Package.objects.create(
            barcode='8234123412341212',
            sender=self.genepeeks,
            recipient=self.lab
        )
        # Notify the permissions manager
        assign_creator(instance=package, user=self.admin)
        package.refresh_from_db()

        self.assertEqual(self.admin, package.creator)
