from api.notificationserializer import NotificationSerializer
from shared.models import Notification
import datetime


class ApiManager:

    def __init__(self):
        self.filters = {
            'last': self.filter_last,
            'reverse': self.filter_reverse,
            'source': self.filter_source,
            'since': self.filter_since,
            'date': self.filter_date,
            'daterange': self.filter_daterange,
            'intitle': self.filter_intitle,
            'incontent': self.filter_incontent,
            'contains': self.filter_contains
        }

    def get(self, params):
        notifications = Notification.objects.all().order_by('-date')

        for filter, func in self.filters.items():
            if filter in params:
                notifications = func(notifications, params[filter])

        return NotificationSerializer(notifications, many=True).data

    def filter_last(self, notifications, param):
        return notifications[:int(param)]

    def filter_reverse(self, notifications, param):
        return notifications[::-1]

    def filter_source(self, notifications, param):
        return notifications.filter(source=param)

    def filter_since(self, notifications, param):
        year, month, day = map(int, param.split("-"))
        return notifications.filter(date__range=[datetime.date(year, month, day), datetime.date.today()])

    def filter_date(self, notifications, param):
        year, month, day = map(int, param.split("-"))
        return notifications.filter(date__date=datetime.date(year, month, day))

    def filter_daterange(self, notifications, param):
        first_date,  second_date = param.split(':')
        first_date = datetime.date(*map(int, first_date.split('-')))
        second_date = datetime.date(*map(int, second_date.split('-')))
        if first_date > second_date:
            first_date, second_date = second_date, first_date
        second_date += datetime.timedelta(days=1)

        return notifications.filter(date__range=[first_date, second_date])

    def filter_intitle(self, notifications, param):
        return notifications.filter(title__contains=param)

    def filter_incontent(self, notifications, param):
        return notifications.filter(content__contains=param)

    def filter_contains(self, notifications, param):
        return notifications.filter(title__contains=param) | notifications.filter(content__contains=param)


