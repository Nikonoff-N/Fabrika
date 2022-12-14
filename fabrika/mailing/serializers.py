
from rest_framework import serializers
from django.contrib.auth.models import User

from mailing.models import Mail,Client

class MailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mail
        fields = ['id', 'pub_date', 'message_text', 'code_filter','tag_filter','end_time']

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ['id', 'phone', 'code', 'tag','timezone']

class UserSerializer(serializers.ModelSerializer):
    mails = serializers.PrimaryKeyRelatedField(many=True, queryset=Mail.objects.all())

    class Meta:
        model = User
        fields = ['id', 'username', 'mails']

class MailStatSerializer(serializers.Serializer):
    total_mails = serializers.IntegerField()
    total_messages = serializers.IntegerField()
    total_send = serializers.IntegerField()
    total_failed = serializers.IntegerField()

class OneMailStatSerializer(serializers.Serializer):
    total_messages = serializers.IntegerField()
    total_send = serializers.IntegerField()
    total_failed = serializers.IntegerField()