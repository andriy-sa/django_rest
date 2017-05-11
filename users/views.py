from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
)
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer, CreateUserSerializer
from django.db.models import Q, Count
from django_rest.helpers import prepare_order, CustomPagination
from rest_framework.response import Response


class UsersListAPIView(ListAPIView):
    serializer_class = UserSerializer
    pagination_class = CustomPagination

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


class CustomRetrive(RetrieveAPIView):
    def retrieve(self, request, *args, **kwargs):
        return Response({'test_data': 'test....'})
