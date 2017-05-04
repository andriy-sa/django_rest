from rest_framework.serializers import ModelSerializer
from .models import Post
from users.models import User


class UserRelationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'is_staff', 'created_at', 'last_login']


class PostSerializer(ModelSerializer):
    user = UserRelationSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'user']
