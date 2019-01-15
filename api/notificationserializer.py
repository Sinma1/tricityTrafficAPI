from rest_framework import serializers

from shared.models import Notification


class NotificationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=60)
    content = serializers.CharField()
    date = serializers.DateTimeField()
    source = serializers.CharField(max_length=50)
