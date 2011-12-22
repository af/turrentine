import os
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _


from turrentine import settings as turrentine_settings


class ChangeableContent(models.Model):
    """
    Abstract base class that provides creation/modification information for content.
    """
    created_at = models.DateTimeField(auto_now_add=True)    # TODO: set this in the admin form
    created_by = models.ForeignKey(User, related_name='+')
    last_modified_at = models.DateTimeField(auto_now=True)
    last_modified_by = models.ForeignKey(User, related_name='+')

    class Meta:
        abstract = True



class CMSPageManager(models.Manager):
    """
    Adds convenience methods for querying CMSPage objects.
    """
    def published(self):
        return self.get_query_set().filter(is_published=True)

    @staticmethod
    def ensure_absolute_url(url_value):
        """
        Validator function that ensures a url string is absolute (starts with a slash).
        """
        if not url_value.startswith('/'):
            raise ValidationError(_('URLs need to be absolute (they should start with a "/").'))

    def create(self, *args, **kwargs):
        """
        Allow an 'author' kwarg to automatically fill in the created_by and last_modified_by fields.
        """
        if kwargs.has_key('author'):
            kwargs['created_by'] = kwargs['author']
            kwargs['last_modified_by'] = kwargs['author']
            del kwargs['author']
        return super(CMSPageManager, self).create(*args, **kwargs)



class CMSPage(ChangeableContent):
    """
    A page in the CMS. This is an elaboration on Django's flatpage model.
    """
    url = models.CharField(_('URL'), max_length=100, unique=True, db_index=True,
                           validators=[CMSPageManager.ensure_absolute_url,],
                           help_text=_('This should be an absolute URL (beginning with a "/")'))
    title = models.CharField(_('title'), max_length=200)
    content = models.TextField(_('content'), blank=True)
    template_name = models.CharField(_('template name'), max_length=70, blank=True)     # TODO: handle default value

    # BooleanFields that limit access to content:
    is_published = models.BooleanField(_('Published'), default=True)
    login_required = models.BooleanField(_('Login Required'), help_text=_('Only allow logged-in users to view the page.'))
    staff_only = models.BooleanField(_('Staff only'), help_text=_('Only allow staff users to access this page.'))

    # SEO-related fields:
    meta_description = models.TextField(_('Meta description'), blank=True,
                                        help_text=_('Will be placed in a meta description tag'))
    meta_keywords = models.CharField(_('Meta keywords'), max_length=300, blank=True,
                                     help_text=_('Will be placed in a meta keywords tag'))

    objects = CMSPageManager()

    class Meta:
        verbose_name = _('CMS Page')
        ordering = ('url',)

    def __unicode__(self):
        return u"%s -- %s" % (self.url, self.title)

    def get_absolute_url(self):
        return self.url

    @staticmethod
    def get_template_options():
        """
        Returns a list of all templates that can be used for CMS pages.
        The paths that are returned are relative to TURRENTINE_TEMPLATE_ROOT.
        """
        template_root = turrentine_settings.TURRENTINE_TEMPLATE_ROOT
        turrentine_dir = turrentine_settings.TURRENTINE_TEMPLATE_SUBDIR
        output = []
        for root, dirs, files in os.walk(turrentine_dir):
            for file_name in files: 
                full_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(full_path, template_root)
                output.append(relative_path)
        return output


class FileUpload(ChangeableContent):
    """
    Simple wrapper model for a CMS-uploaded file.
    """
    file = models.FileField(upload_to=turrentine_settings.TURRENTINE_UPLOAD_DIR)

    def __unicode__(self):
        upload_prefix = turrentine_settings.TURRENTINE_UPLOAD_DIR + '/'
        return self.file.name.strip(upload_prefix)

    @property
    def url(self):
        return self.file.url

@receiver(models.signals.pre_delete, sender=FileUpload)
def cleanup_answer_on_delete(sender, **kwargs):
    """
    Delete the file from the filesystem when a FileUpload is deleted.
    """
    instance = kwargs['instance']
    instance.file.delete()
