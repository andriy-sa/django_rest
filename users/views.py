from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import User
from .serializers import UserSerializer
from django.db.models import Q, Prefetch
from django_rest.helpers import prepare_order
from posts.models import Post


class UsersListAPIView(ListAPIView):
    serializer_class = UserSerializer
    pagination_class = None

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        sort = self.request.GET.get('sort', '-created_at')
        available_sorts = ['created_at', '-created_at', 'last_login', '-last_login', 'email', '-email', 'username',
                           '-username']
        sort = prepare_order(sort, available_sorts, '-created_at')
        queryset = User.objects.all()

        if q:
            queryset = queryset.filter(Q(username__icontains=q) | Q(email__icontains=q))

        return queryset.order_by(sort).prefetch_related(Prefetch('posts', queryset=Post.objects.filter(id__gt=1)))


class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
