from django.conf.urls import url
from .views import index

urlpatterns = [
    url(r'^io$', index, name='test_sockets'),
]
