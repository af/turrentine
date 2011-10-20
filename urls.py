from django.conf.urls.defaults import patterns
from turrentine.views import PageView

urlpatterns = patterns('turrentine.views',
    (r'^(?P<path>.*)$', PageView.as_view()),
)
