from rest_framework.serializers import ModelSerializer, Serializer, CharField, IntegerField, DateTimeField
from users.models import User


class UserStatsSerializer(ModelSerializer):
    #first_login = DateTimeField()
    login_last = DateTimeField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'login_last']
