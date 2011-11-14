from django.conf import settings
from django.http import Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.views.generic import DetailView

from turrentine import settings as turrentine_settings
from turrentine.models import CMSPage


class PageView(DetailView):
    """
    Render a CMS page, using django's generic DetailView.
    """
    context_object_name = 'page'

    def get_queryset(self):
        return CMSPage.objects.published()

    def get_object(self, queryset=None):
        url = self.kwargs.get('path', '')
        if not url.startswith('/'):
            url = '/' + url
        try:
            page = CMSPage.objects.published().get(url=url)
            # Mark the html content as safe so we don't have to use the safe
            # template tag in all cms templates:
            page.title = mark_safe(page.title)
            page.content = mark_safe(page.content)
            return page
        except CMSPage.DoesNotExist:
            raise Http404

    def get_template_names(self):
        """
        Return the page's specified template name, or a fallback if one hasn't been chosen.
        """
        name = self.object.template_name or turrentine_settings.TURRENTINE_TEMPLATE_FALLBACK
        return [name,]

    def get_mimetype(self):
        """
        Use the ending of the template name to infer response's Content-Type header.
        """
        template_name = self.get_template_names()[0]
        for extension, mimetype in turrentine_settings.TURRENTINE_MIMETYPE_EXTENSIONS:
            if template_name.endswith(extension):
                return mimetype
        return 'text/html'      # Fallback to text/html if nothing matches

    def get(self, request, *args, **kwargs):
        """
        Check user authentication if the page requires a login.

        We could do this by overriding dispatch() instead, but we assume
        that only GET requests will be required by the CMS pages.
        """
        try:
            page = self.object = self.get_object()
        except Http404:
            # If APPEND_SLASH is set and our url has no trailing slash,
            # look for a CMS page at the alternate url:
            if settings.APPEND_SLASH and not self.kwargs.get('path', '/').endswith('/'):
                return self._try_url_with_appended_slash()
            else:
                raise Http404

        # Check request.user's credentials in accessing this page:
        if page.staff_only and not request.user.is_staff:
            # Block out non-staff users on restricted pages.
            # Django 1.4 will introduce better HTTP 403 support, but until then
            # we'll just render a plain "permission denied" template (which can be overridden):
            return render(request, 'turrentine/403.html', status=403)
        if page.login_required and request.user.is_anonymous():
            redirect_url = '%s?next=%s' % (settings.LOGIN_URL, self.kwargs.get('path', ''))
            return HttpResponseRedirect(redirect_url)
        else:
            context = self.get_context_data(object=self.object)
            return self.render_to_response(context, content_type=self.get_mimetype())

    def _try_url_with_appended_slash(self):
        """
        Try our URL with an appended slash. If a CMS page is found at that URL, redirect to it.
        If no page is found at that URL, raise Http404.
        """
        new_url_to_try = self.kwargs.get('path', '') + '/'
        if not new_url_to_try.startswith('/'):
            new_url_to_try = '/' + new_url_to_try
        if CMSPage.objects.published().filter(url=new_url_to_try).exists():
            return HttpResponsePermanentRedirect(new_url_to_try)
        else:
            raise Http404
