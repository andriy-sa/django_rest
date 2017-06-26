from django.conf.urls import url
from .views import PostsListAPIView, PostDetailAPIView, CommentCreateAPIView, CommentsListAPIView

urlpatterns = [
    url(r'^posts/list$', PostsListAPIView.as_view(), name='list'),
    url(r'^posts/(?P<pk>\+d)$', PostDetailAPIView.as_view(), name='get_by_id'),
    url(r'^posts/comment$', CommentCreateAPIView.as_view(), name='comment_create'),
    url(r'^posts/(?P<pk>\d+)/comments$', CommentsListAPIView.as_view(), name='comments_list'),
]
