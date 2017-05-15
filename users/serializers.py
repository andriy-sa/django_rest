from rest_framework.serializers import ModelSerializer, Serializer, IntegerField, CharField, ValidationError
from .models import User
from posts.models import Post
from django.contrib.auth import authenticate


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


class UpdateUserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username',
                  'email']


class LoginSerializer(Serializer):
    email = CharField(max_length=255, required=False)
    username = CharField(max_length=255, read_only=True)
    password = CharField(max_length=128, write_only=True, required=False)
    token = CharField(max_length=255, read_only=True)

    def validate(self, data):

        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=email, password=password)

        if user is None:
            raise ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise ValidationError(
                'This user has been deactivated.'
            )

        return {
            'token': user.token
        }
