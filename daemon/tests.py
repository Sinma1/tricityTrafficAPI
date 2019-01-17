from datetime import datetime

from django.test import TestCase

# Create your tests here.
from daemon.helpers import create_notification
from shared.models import Notification


class HelperTest(TestCase):
    def test_create_notification(self):
        title = "Title"
        content = "Example content"
        date = datetime(2019, 1, 8)
        source = "Trusted source"

        self.assertEqual(Notification(title=title, content=content, date=date, source=source),
                         create_notification(title, content, date, source))
