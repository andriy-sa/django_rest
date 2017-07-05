from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
#from rest_framework_swagger.views import get_swagger_view
from .swagger import SwaggerSchemaView
from rest_framework.documentation import include_docs_urls

from django.conf.urls import handler404

handler404 = 'django_rest.errors.error404'

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('users.urls', namespace='users')),
    url(r'^api/', include('posts.urls', namespace='posts')),
    url(r'^api/', include('statistic.urls', namespace='stats')),
    url(r'^docs/$', SwaggerSchemaView.as_view()),
    url(r'^docs2/', include('rest_framework_docs.urls')),
    url(r'^docs3/', include_docs_urls(title='My API title')),
    url(r'^', include('socket_io.urls', namespace='sockets')),
]



if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]