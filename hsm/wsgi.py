"""
WSGI config for hsm project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

PRODUCTION = os.environ.get('ENV') == 'production'

if PRODUCTION:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hsm.settings.production')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hsm.settings.development')

application = get_wsgi_application()
