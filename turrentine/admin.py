from urlparse import urljoin
from django import forms
from django.conf import settings
from django.conf.urls.defaults import patterns
from django.contrib import admin

from turrentine.models import CMSPage, FileUpload
from turrentine.views import PageView

# If django-reversion is installed, use its VersionAdmin as an admin base class:
try:
    import reversion
    admin_base_class = reversion.VersionAdmin
except ImportError:
    admin_base_class = admin.ModelAdmin


class ChangeableContentForm(forms.ModelForm):
    def save(self, *args, **kwargs):
        """
        Save the created_by and last_modified_by fields based on the current admin user.
        """
        if not self.instance.id:
            self.instance.created_by = self.user
        self.instance.last_modified_by = self.user
        return super(ChangeableContentForm, self).save(*args, **kwargs)


class PageAdminForm(ChangeableContentForm):
    """
    Form class to be used when editing CMS pages in the admin.

    The calling code must set a 'user' attribute to the django User that submitted
    the form in the admin.
    """
    template_name = forms.ChoiceField(label='Template', choices=[(t,t) for t in CMSPage.get_template_options()])
    content = forms.CharField(widget=forms.Textarea(), initial='<h1>Enter your page content here</h1>')

    class Meta:
        model = CMSPage

    class Media:
        css = {
            'all': (
                urljoin(settings.STATIC_URL, 'turrentine/css/page_edit.css'),
            )
        }
        js = (
            urljoin(settings.STATIC_URL, 'turrentine/js/iframe_preview.js'),
        )


class FileUploadAdmin(admin.ModelAdmin):
    form = ChangeableContentForm
    list_display = ('__unicode__', 'url', 'created_by', 'created_at')
    exclude = ('created_by', 'last_modified_by',)
    ordering = ('file',)

    def get_form(self, request, obj=None, **kwargs):
         form = super(FileUploadAdmin, self).get_form(request, obj, **kwargs)
         form.user = request.user
         return form
admin.site.register(FileUpload, FileUploadAdmin)


class PageAdmin(admin_base_class):
    form = PageAdminForm

    list_display = ('url', 'title', 'is_published', 'template_name', 'created_by', 'created_at',
                    'last_modified_by', 'last_modified_at', 'staff_only')
    list_display_links = ('title',)
    list_editable = ('is_published',)
    list_filter = ('is_published', 'login_required', 'staff_only', 'created_by',)
    list_select_related = True
    ordering = ('url',)
    save_on_top = True
    search_fields = ('url', 'title',)

    fieldsets = (
        (None, {
            'fields': ('url', 'title', 'template_name',),
        }),
        ('Content', {
            'fields': ('content',),
        }),
        ('Access Control', {
            'fields': ('is_published', 'login_required', 'staff_only',),
            'classes': ('collapse',),
        }),
        ('SEO Fields', {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
         form = super(PageAdmin, self).get_form(request, obj, **kwargs)
         form.user = request.user
         return form

    def get_urls(self):
        """
        Add our preview view to our urls.
        """
        urls = super(PageAdmin, self).get_urls()
        my_urls = patterns('',
            (r'^add/preview$', self.admin_site.admin_view(PagePreviewView.as_view())),
            (r'^(?P<id>\d+)/preview$', self.admin_site.admin_view(PagePreviewView.as_view())),
            (r'^(?P<id>\d+)/history/(\d+)/preview$', self.admin_site.admin_view(PagePreviewView.as_view())),
        )
        return my_urls + urls

admin.site.register(CMSPage, PageAdmin)


class PagePreviewView(PageView):
    """
    Subclass of PageView that supports POST requests for admin previews.

    It accepts POST parameters for the page's title and content, and returns the page
    with this data substituded in.
    """

    def get_object(self, queryset=None):
        from django.shortcuts import get_object_or_404
        id = self.kwargs.get('id', 0)
        if id:
            page = get_object_or_404(CMSPage, id=self.kwargs.get('id', 0))
        else:
            # Handle the case where the preview is invoked from the "add" page.
            # No CMSPage instance will have been saved yet, so create a new one:
            page = CMSPage()
        return page

    def get_template_names(self):
        """
        Return the page's specified template name, or a fallback if one hasn't been chosen.
        """
        posted_name = self.request.POST.get('template_name')
        if posted_name:
            return [posted_name,]
        else:
            return super(PagePreviewView, self).get_template_names()

    def post(self, request, *args, **kwargs):
        """
        Accepts POST requests, and substitute the data in for the page's attributes.
        """
        self.object = self.get_object()
        self.object.content = request.POST['content']
        self.object.title = request.POST['title']

        self.object = self._mark_html_fields_as_safe(self.object)
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context, content_type=self.get_mimetype())
