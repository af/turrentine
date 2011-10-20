from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import ugettext_lazy as _


def ensure_absolute_url(url_value):
    """
    Ensure that a url string is absolute (starts with a slash).
    """
    if not url_value.startswith('/'):
        raise ValidationError(_('URLs need to be absolute (they should start with a "/").'))


class CMSPageManager(models.Manager):
    """
    Adds convenience methods for querying CMSPage objects.
    """
    def published(self):
        return self.get_query_set().filter(is_published=True)


class CMSPage(models.Model):
    """
    A page in the CMS. This is an elaboration on Django's flatpage model.
    """
    url = models.CharField(_('URL'), max_length=100, unique=True, db_index=True, validators=[ensure_absolute_url,])
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'), blank=True)
    template_name = models.CharField(_('template name'), max_length=70, blank=True)     # TODO: handle default value
    is_published = models.BooleanField(_('is published'), default=True)
    login_required = models.BooleanField(_('login required'), help_text=_("Only allow logged-in users to view the page."))

    # SEO-related fields:
    meta_description = models.TextField(_('SEO description'), blank=True,
                                        help_text=_('Will be placed in a meta description tag'))
    meta_keywords = models.CharField(_('SEO keywords'), max_length=300, blank=True,
                                     help_text=_('Will be placed in a meta keywords tag'))

    objects = CMSPageManager()

    class Meta:
        verbose_name = _('CMS page')
        ordering = ('url',)

    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url
