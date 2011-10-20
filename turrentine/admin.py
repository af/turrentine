from django.contrib import admin

from turrentine.models import CMSPage

class PageAdmin(admin.ModelAdmin):
    list_display = ('url', 'title', 'template_name')
    fieldsets = (
        (None, {
            'fields': ('url', 'title', 'is_published', 'login_required', 'template_name', 'content'),
        }),
        ('SEO Settings', {
            'classes': ('collapse',),
            'fields': ('meta_description', 'meta_keywords'),
        }),
    )
admin.site.register(CMSPage, PageAdmin)
