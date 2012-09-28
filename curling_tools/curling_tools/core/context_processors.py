# -*- coding: utf-8 -*-
from django.conf import settings

def site_infos(request):
    """
    Get some basics informations about the app.
    """
    return {'SITE_NAME': settings.SITE_NAME}
