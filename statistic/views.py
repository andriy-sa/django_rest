from rest_framework.generics import ListAPIView

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
from django.db.models import Max, Min, OuterRef, Subquery
from .serializers import UserStatsSerializer
from datetime import datetime
from django.db.models.expressions import RawSQL
import pendulum
from .models import Statistic



class StatisticAPIView(APIView):
    def get(self, request):
        date = pendulum.now().subtract(months=1).to_datetime_string()
        # subquery = "select s.created_at from statistic_statistic as s where s.created_at > %s and s.user_id = users_user.id order by s.created_at desc limit 1"

        # users = User.objects.only("id", "username","email").annotate(login_last=RawSQL(subquery,(date,)))
        last_login = Statistic.objects.filter(created_at__gt=date, user_id=OuterRef('pk')).order_by('-created_at')
        users = User.objects.only("id", "username", "email") \
            .annotate(login_last=Subquery(last_login.values('created_at')[:1]))

        # .annotate(first_login=Min('statistic__created_at'))

        # subquery = "select s.created_at from statistic_statistic as s where s.created_at > %s and s.user_id = users_user.id order by s.created_at desc limit 1"
        # users = users.extra(select = {'last_login': subquery},select_params = (date,))


        print(users.query)
        response = UserStatsSerializer(users, many=True).data
        return Response(response, 200)
