from .models import Post
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import PostSerializer
from django_rest.helpers import prepare_order, CustomPagination
from django.db.models import Q


class PostsListAPIView(ListAPIView):
    serializer_class = PostSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Post.objects.all()

        q = self.request.GET.get('q', '')
        sort = self.request.GET.get('sort', '-created_at')
        available_sorts = ['created_at', '-created_at', 'title', '-title']
        sort = prepare_order(sort, available_sorts, '-created_at')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(user__username__icontains=q) | Q(user__email__icontains=q))

        return queryset.prefetch_related('user').order_by(sort)


class PostDetailAPIView(RetrieveAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all().prefetch_related('user')
