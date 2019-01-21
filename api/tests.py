from datetime import datetime

from django.test import TestCase

# Create your tests here.
from django.urls import reverse, resolve

from api.apimanager import ApiManager
from shared.models import Notification


class ApiTests(TestCase):
    def setUp(self):
        Notification.objects.create(title="1", content="Test notification 1", source="source1",
                                    date=datetime(2019, 1, 15))
        Notification.objects.create(title="2", content="Example notification 2", source="source2",
                                    date=datetime(2019, 1, 16))
        Notification.objects.create(title="3", content="Simple notification 3", source="source3",
                                    date=datetime(2019, 1, 17))

    def test_api_status_code(self):
        url = reverse('api:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_api_parameter_intitle(self):
        response = self.client.get('/api/?intitle=1')
        self.assertContains(response, 'Test')

    def test_api_parameter_source(self):
        response = self.client.get('/api/?source=source3')
        self.assertContains(response, 'Simple')


class ApiManagerTest(TestCase):
    def setUp(self):
        Notification.objects.create(title="1", content="Test notification 1", source="source1",
                                    date=datetime(2019, 1, 15))
        Notification.objects.create(title="2", content="Example notification 2", source="source2",
                                    date=datetime(2019, 1, 16))
        Notification.objects.create(title="3", content="Simple notification 3", source="source3",
                                    date=datetime(2019, 1, 17))
        self.api = ApiManager()
        self.notifications = Notification.objects.all()

    def test_filter_last(self):
        notifications = self.api.filter_last(self.notifications, 2)
        self.assertEqual(len(notifications), 2)

        notifications = self.api.filter_last(self.notifications, 1)
        self.assertEqual(len(notifications), 1)

    def test_filter_date(self):
        notifications = self.api.filter_date(self.notifications, "2019-01-16")
        for notification in notifications:
            self.assertEqual(notification.date, datetime(2019, 1, 16))

    def test_filter_source(self):
        notifications = self.api.filter_source(self.notifications, 'source1')
        for notification in notifications:
            self.assertEqual(notification.source, 'source1')

    def test_filter_incontent(self):
        notifications = self.api.filter_incontent(self.notifications, 'simple')
        for notification in notifications:
            self.assertNotEqual(notification.content.lower().find('simple'), -1)

    def test_filter_intitle(self):
        notifications = self.api.filter_intitle(self.notifications, '1')
        for notification in notifications:
            self.assertNotEqual(notification.title.lower().find('1'), -1)

    def test_filter_contains(self):
        notifications = self.api.filter_contains(self.notifications, 'notif')
        for notification in notifications:
            found = (notification.title.lower().find('notif') != -1 or
                     notification.content.lower().find('notif') != -1)
            self.assertTrue(found)
