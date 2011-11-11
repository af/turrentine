import os.path
from django.conf import settings

# The directory where you keep your templates.
# For most people, this will be $PROJECT_ROOT/templates
template_dir_guess = getattr(settings, 'TEMPLATE_DIRS', ('templates',))[0]
TURRENTINE_TEMPLATE_ROOT = getattr(settings, 'TURRENTINE_TEMPLATE_ROOT', template_dir_guess)

# The directory where turrentine looks for templates that can be given as options
# for CMS pages in the admin. Defaults to a relative location of '/cms/', but
# you can override this to whatever you want:
default_setting = os.path.join(TURRENTINE_TEMPLATE_ROOT, 'cms')
TURRENTINE_TEMPLATE_SUBDIR = getattr(settings, 'TURRENTINE_TEMPLATE_ROOT', default_setting)

# The template to use for rendering a page if CMSPage.template_name is not specified:
TURRENTINE_TEMPLATE_FALLBACK = getattr(settings, 'TURRENTINE_TEMPLATE_ROOT', 'turrentine/fallback.html')

# The amount of time (in seconds) to cache CMS pages, if caching is enabled.
# Disabled (time = 0) by default, so override this in settings.py to enable caching.
TURRENTINE_PAGE_CACHE_TIME = getattr(settings, 'TURRENTINE_PAGE_CACHE_TIME', 0)
