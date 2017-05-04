from django.conf.urls import url
from .views import PostsListAPIView, PostDetailAPIView

urlpatterns = [
    url(r'^posts/list', PostsListAPIView.as_view(), name='list'),
    url(r'^posts/(?P<pk>[\d])', PostDetailAPIView.as_view(), name='get_by_id'),
]
