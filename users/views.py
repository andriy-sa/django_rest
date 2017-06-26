from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView
)
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated
)
from .serializers import (
    UserSerializer,
    CreateUserSerializer,
    UpdateUserSerializer,
    LoginSerializer,
)
from rest_framework.views import APIView
from .models import User
from django.db.models import Q, Count
from django_rest.helpers import prepare_order, CustomPagination
from rest_framework.response import Response
import coreapi

class UsersListAPIView(ListAPIView):
    #permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    pagination_class = CustomPagination
    model = User
    coreapi_fields = (
        coreapi.Field(
            name='q',
            location='query',
            required=False,
            description='Search field',
            type='string'
        ),
        coreapi.Field(
            name='sort',
            location='query',
            required=False,
            description='Sort field',
            type='string'
        ),
    )

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        sort = self.request.GET.get('sort', '-created_at')
        available_sorts = ['created_at', '-created_at', 'last_login', '-last_login', 'email', '-email', 'username',
                           '-username']
        sort = prepare_order(sort, available_sorts, '-created_at')
        queryset = User.objects.all()

        if q:
            queryset = queryset.filter(Q(username__icontains=q) | Q(email__icontains=q))

        # return queryset.order_by(sort).prefetch_related(Prefetch('posts', queryset=Post.objects.filter(id__gt=1)))
        return queryset.order_by(sort).prefetch_related('posts').annotate(Count('posts'))


class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateAPIView(APIView):
    serializer_class = CreateUserSerializer

    def post(self, request):
        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        user = User(**serializer.data)
        user.set_password(serializer.data.get('password'))
        user.save()

        response = UserSerializer(instance=user).data
        response['token'] = user.token

        return Response(response, status=200)


class UserUpdateAPIView(APIView):
    serializer_class = UpdateUserSerializer

    def put(self, request, id):
        user = User.objects.filter(id=id).first()
        if not user:
            return Response({}, status=404)

        data = request.data

        serializer = self.serializer_class(user, data=data)
        serializer.is_valid(raise_exception=True)

        user.username = serializer.initial_data.get('username')
        user.email = serializer.initial_data.get('email')
        user.save()

        return Response(UserSerializer(instance=user).data, status=200)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer
    coreapi_fields = (
        coreapi.Field(
            name='data',
            location='body',
            required=True,
            type='array'
        ),
    )

    def get_serializer_class(self):
        return self.serializer_class

    def post(self, request):
        """
            Example Request:
                - body:{
                    'email': string (required),
                    'password': string (required)
                }

            responseMessages:
                - code: 200
                   token: (string) 
                - code: 401
                    message: (string)
            """

        data = request.data

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=200)


class MeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(UserSerializer(instance=request.user).data, status=200)


class CustomRetrive(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        return Response({'test_data': 'test....'})
