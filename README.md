Turrentine
==========

Turrentine is a simple content management app for Django. What, *another* CMS
app? Yes, but I tried several before deciding that I couldn't find one with a few more
features than flatpages, but not much more.

### Turrentine is:

* Simple: very little code, and few features by design.
* Dependency-free, unlike some other "simple" CMS apps that still require you
  to pull in 3-5 other packages.
* Easy on the database. A user viewing a CMS page should never generate more
  than one or two simple database queries.
* Kind of a half-way point between Django's basic flatpages app, and other simple
  third-party CMSes like gnocchi-cms.

### Things Turrentine does **not** do:

* Tree-like page hierarchies. Like flatpages, with turrentine you just specify
  the page's URL directly.
* WYSIWYG editing
* File uploads in the admin (add something like `django-adminfiles`,
  `django-admin-uploads`, or `django-filebrowser` if you need that).
* Auto-generated menus
* Template editing in the admin
* Internationalization (although this might be worth adding later)

### Consider Turrentine if...

* You don't need any of the stuff in the previous section
* You want a simple CMS app that is easy to configure, and for the most part
  just gets out of your way.
* You have page authors who are comfortable writing html, but you don't want
  them to have to write django templates. You have developers/designers that
  can develop your templates for the CMS.


Setup
------

# Install turrentine.   #TODO: add instructions using pip
# Add 'turrentine' to your installed apps in settings.py:

    INSTALLED_APPS = (
        # Your other apps here
        'turrentine',
    )

# Add turrentine at the **end** of your root urlconf:

    urlpatterns = patterns('',
        # Your other urls go here

        (r'^', include('turrentine.urls')),
    )


# Also in settings.py, define a `CMS_TEMPLATE_ROOT`. This is the directory on
your filesystem where Turrentine looks for CMS template files. The following
will probably work for your project:

    import os.path
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    CMS_TEMPLATE_ROOT = os.path.join(PROJECT_ROOT, 'templates', 'cms')

# As indicated in the previous step, create a directory for your CMS templates:

    mkdir -p templates/cms

# Create template(s) in your `CMS_TEMPLATE_ROOT`, so they can be used by your pages.
  You'll probably want to use the following template variables:

  * `{{ page.title }}`
  * `{{ page.content }}`
  * `{{ page.meta_description }}`
  * `{{ page.meta_keywords }}`
