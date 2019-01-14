from daemon.dataSources import TrojmiastoDataSource
from shared.models import Notification

class Fetcher:
    def __init__(self):
        self.sources = [
            TrojmiastoDataSource
        ]

    def fetch(self):
        try:
            last_fetch = Notification.objects.latest('date').date
        except Notification.DoesNotExist:
            last_fetch = None

        for source in self.sources:
            try:
                s = source()
                for notification in s.get_data(last_fetch):
                    notification.save()
            except:
                pass
