"""View decorators."""
import unittest

from django.conf import settings


def selenium_test(function):
    """Decorator to determine whether selenium tests should be executed.
    """
    return function if settings.RUN_LIVE_TESTS else unittest.skip("Selenium tests not enabled.")
