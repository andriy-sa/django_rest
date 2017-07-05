from django.conf.urls import url
from .views import StatisticAPIView

urlpatterns = [
    url(r'^statistic', StatisticAPIView.as_view(), name='list'),
]
