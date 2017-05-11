from rest_framework.serializers import ModelSerializer, IntegerField, CharField, ValidationError
from .models import User
from posts.models import Post


class PostRelationSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'description', 'created_at', 'updated_at']


class UserSerializer(ModelSerializer):
    posts = PostRelationSerializer(read_only=True, many=True)
    posts__count = IntegerField(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'is_staff', 'created_at', 'last_login', 'posts__count',
                  'posts']


class CreateUserSerializer(ModelSerializer):
    password = CharField(
        max_length=128,
        min_length=8
    )
    password_confirm = CharField(write_only=True)

    def validate_password_confirm(self, value):
        password = self.initial_data.get('password')

        if password != value:
            raise ValidationError("Password Confirm not match password field.")

        return value

    class Meta:
        model = User
        fields = ['username',
                  'email',
                  'password',
                  'password_confirm']