import os.path
from django.conf import settings

# The directory where you keep your templates.
# For most people, this will be $PROJECT_ROOT/templates
template_dir_guess = getattr(settings, 'TEMPLATE_DIRS', ('templates',))[0]
TURRENTINE_TEMPLATE_ROOT = getattr(settings, 'TURRENTINE_TEMPLATE_ROOT', template_dir_guess)

# The directory where turrentine looks for templates that can be given as options
# for CMS pages in the admin. Defaults to a TURRENTINE_TEMPLATE_ROOT subdir named
# 'cms', but you can override this to be whatever you want:
default_setting = os.path.join(TURRENTINE_TEMPLATE_ROOT, 'cms')
TURRENTINE_TEMPLATE_SUBDIR = getattr(settings, 'TURRENTINE_TEMPLATE_SUBDIR', default_setting)

# The template to use for rendering a page if CMSPage.template_name is not specified:
TURRENTINE_TEMPLATE_FALLBACK = getattr(settings, 'TURRENTINE_TEMPLATE_FALLBACK', 'turrentine/fallback.html')

# List of MIME types to infer, based on the extension of the template name that was used:
TURRENTINE_MIMETYPE_EXTENSIONS = getattr(settings, 'TURRENTINE_MIMETYPE_EXTENSIONS', (
    ('.html', 'text/html'),
    ('.js', 'text/javascript'),
    ('.json', 'application/json'),
    ('.txt', 'text/plain'),
    ('.xhtml', 'application/xhtml+xml'),
    ('.xml', 'application/xml'),
))
