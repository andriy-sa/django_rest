from django.conf.urls import url
from users.views import (
    UsersListAPIView,
    UserDetailAPIView,
    UserCreateAPIView,
    UserUpdateAPIView,
    CustomRetrive,
    LoginAPIView,
    MeAPIView
)

urlpatterns = [
    url(r'^users/$', UsersListAPIView.as_view(), name='list'),
    url(r'^users/(?P<pk>\d+)$', UserDetailAPIView.as_view(), name='get_by_id'),
    url(r'^users/create/$', UserCreateAPIView.as_view(), name='create'),
    url(r'^users/update/(?P<id>\d+)$', UserUpdateAPIView.as_view(), name='update'),
    url(r'^login$', LoginAPIView.as_view(), name='login'),
    url(r'^check$', MeAPIView.as_view(), name='check'),
    url(r'^get_custom', CustomRetrive.as_view(), name='get_custom'),
]
