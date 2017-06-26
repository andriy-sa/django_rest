"""django_rest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
#from rest_framework_swagger.views import get_swagger_view
from .swagger import SwaggerSchemaView
from rest_framework.documentation import include_docs_urls
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include('users.urls', namespace='users')),
    url(r'^api/', include('posts.urls', namespace='posts')),
    url(r'^docs/$', SwaggerSchemaView.as_view()),
    url(r'^docs2/', include('rest_framework_docs.urls')),
    url(r'^docs3/', include_docs_urls(title='My API title'))
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]