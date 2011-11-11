from urlparse import urljoin
from django import forms
from django.conf import settings
from django.contrib import admin

from turrentine.models import CMSPage


class PageAdminForm(forms.ModelForm):
    """
    Form class to be used when editing CMS pages in the admin.

    The calling code must set a 'user' attribute to the django User that submitted
    the form in the admin.
    """
    template_name = forms.ChoiceField(label='Template', choices=[(t,t) for t in CMSPage.get_template_options()])

    class Meta:
        model = CMSPage

    class Media:
        css = {
            'all': (
                urljoin(settings.STATIC_URL, 'turrentine/css/page_edit.css'),
            )
        }

    def save(self, *args, **kwargs):
        """
        Save the created_by and last_modified_by fields based on the current admin user.
        """
        if not self.instance.id:
            self.instance.created_by = self.user
        self.instance.last_modified_by = self.user
        return super(PageAdminForm, self).save(*args, **kwargs)


class PageAdmin(admin.ModelAdmin):
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
            'fields': ('url', 'title', 'is_published', 'login_required', 'staff_only', 'template_name', 'content'),
        }),
        ('SEO Settings', {
            'classes': ('collapse',),
            'fields': ('meta_description', 'meta_keywords'),
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
         form = super(PageAdmin, self).get_form(request, obj, **kwargs)
         form.user = request.user
         return form
admin.site.register(CMSPage, PageAdmin)
