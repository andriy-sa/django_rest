from rest_framework.serializers import ModelSerializer
from .models import User
from posts.models import Post


class PostRelationSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_at', 'updated_at']


class UserSerializer(ModelSerializer):
    posts = PostRelationSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'is_staff', 'created_at', 'last_login', 'posts']
