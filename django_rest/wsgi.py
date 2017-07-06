"""
WSGI config for django_rest project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_rest.settings")

from django.core.wsgi import get_wsgi_application
from whitenoise.django import DjangoWhiteNoise

import socketio
from socketio import Middleware
sio = socketio.Server(async_mode='eventlet')

application = get_wsgi_application()
application = DjangoWhiteNoise(application)
application = Middleware(sio,application)