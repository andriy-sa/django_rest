from rest_framework.serializers import ModelSerializer, Serializer, CharField, IntegerField
from .models import Post, Comment
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


class CommentCreateSerializer(Serializer):
    name = CharField(max_length=255, required=True)
    text = CharField(required=True)
    post_id = IntegerField(required=True)
    parent_id = IntegerField(allow_null=True)
