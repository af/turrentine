import os.path
from django.conf import settings

template_root = getattr(settings, 'TEMPLATE_DIRS', ('templates',))[0]
default_setting = os.path.join(template_root, 'cms')

# The directory where turrentine looks for templates that can be given as options
# for CMS pages in the admin. Tries to guess a location of 'templates/cms/', but
# you probably want to override this in your own settings.py:
TURRENTINE_TEMPLATE_ROOT = getattr(settings, 'TURRENTINE_TEMPLATE_ROOT', default_setting)

# The template to use for rendering a page if CMSPage.template_name is not specified:
TURRENTINE_TEMPLATE_FALLBACK = getattr(settings, 'TURRENTINE_TEMPLATE_ROOT', 'turrentine/fallback.html')
