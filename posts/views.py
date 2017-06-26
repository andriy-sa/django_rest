from .models import Post, Comment
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import PostSerializer, CommentCreateSerializer
from django_rest.helpers import prepare_order, CustomPagination
from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView


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


class CommentCreateAPIView(APIView):
    serializer_class = CommentCreateSerializer

    def post(self, request):
        data = request.data

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        if data['parent_id'] is None:
            Comment.add_root(post_id=data['post_id'], name=data['name'], text=data['text'])
        else:
            Comment.objects.get(pk=data['parent_id']).add_child(post_id=data['post_id'], name=data['name'],
                                                                text=data['text'])

        return Response(data, status=201)


class CommentsListAPIView(APIView):

    def get(self, request, pk):
        post = Post.objects.filter(id=pk).first()
        if not post:
            return Response({}, status=404)

        comments = Comment.dump_bulk(post_id=pk)
        print(comments)
        return Response(comments, status=200)
