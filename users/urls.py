from django.conf.urls import url
from users.views import UsersListAPIView, UserDetailAPIView, UserCreateAPIView, CustomRetrive

urlpatterns = [
    url(r'^users/list', UsersListAPIView.as_view(), name='list'),
    url(r'^users/(?P<pk>[\d])', UserDetailAPIView.as_view(), name='get_by_id'),
    url(r'^users/create', UserCreateAPIView.as_view(), name='create'),
    url(r'^get_custom', CustomRetrive.as_view(), name='get_custom'),
]
