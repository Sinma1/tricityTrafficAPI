from datetime import datetime, timedelta

import requests
from bs4 import BeautifulSoup

from .helpers import create_notification


class TrojmiastoDataSource:
    def __init__(self):
        self.url = "https://trojmiasto.pl/raport"
        self.name = "trojmiasto.pl"

    def get_site(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            raise requests.exceptions.HTTPError

        return response.text

    def parse_to_datetime(self, raport):
        hours, minutes = map(int, raport.find('a').get_text().strip().split(':'))
        now = datetime.now()
        dt = datetime(now.year, now.month, now.day, hours, minutes)
        date = raport.find(class_='date')

        if date is None:
            return dt

        if date.get_text() == "wczoraj":
            dt = dt - timedelta(days=1)
        else:
            day, month, year = map(int, date.get_text().split('.'))
            dt = dt.replace(year=year, month=month, day=day)

        return dt

    def parse_to_notification(self, raport):
        dt = self.parse_to_datetime(raport.find(class_='date-wrap'))
        title = raport.find(class_='report-content-inner').find('a').get_text().strip()
        content = raport.find(class_='text').get_text().strip()
        notification = create_notification(title, content, dt, self.name)

        return notification

    def get_data(self, last_fetch=None):
        response = self.get_site()
        bs = BeautifulSoup(response, 'html.parser')

        result = []
        raports = bs.find_all(class_='report-item')
        for raport in raports:
            notification = self.parse_to_notification(raport)

            if last_fetch and notification.date.replace(tzinfo=None) <= last_fetch.replace(tzinfo=None):
                continue
            from django.utils import timezone
            k = timezone.now()
            result.append(notification)

        return result


class FacebookZepsutyDataSource:
    def __init__(self):
        self.url = "https://www.facebook.com/zepsuty"
        self.name = "facebook.com/zepsuty"

    def get_site(self):
        response = requests.get(self.url)
        if response.status_code != 200:
            raise requests.exceptions.HTTPError

        return response.text

    def parse_to_notification(self, post):
        content = post.find(class_="userContent").get_text().strip()
        date = datetime.fromtimestamp(int(post.find('abbr')['data-utime']))
        notification = create_notification("", content, date, self.name)

        return notification

    def get_data(self, last_fetch=None):
        feed = BeautifulSoup(self.get_site(), 'html.parser')

        posts = []
        for post in feed.find_all(class_="userContent"):
            notification = self.parse_to_notification(post.parent)

            if last_fetch and notification.date <= last_fetch:
                continue

            posts.append(notification)
        return posts
