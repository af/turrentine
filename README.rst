==========
Turrentine
==========

Turrentine is a simple content management app for Django (1.3 and later). It's
designed to allow HTML-savvy users to add and edit pages and files with a minimum of
hassle.

Features
--------

* Live previews while editing pages in the admin (this uses javascript and
  CSS3, so a modern browser is highly recommended).
* Very basic file uploads in the admin.
* Optional version tracking for pages, if you install ``django-reversion``.
* No hard dependencies.
* Easy on the database. A user viewing a CMS page should never generate more
  than one or two simple database queries.

Things Turrentine does **not** do:
----------------------------------

* Tree-like page hierarchies. Like flatpages, with turrentine you just specify
  the page's URL directly.
* WYSIWYG editing. It's assumed that page authors know some basic HTML.
* Auto-generated menus.
* Template editing in the admin.
* Multi-site support.
* Commenting on pages.
* Internationalization (although this might be worth adding later).

Consider Turrentine if...
-------------------------

* You don't need any of the stuff in the previous section.
* You have page authors who are comfortable writing HTML, but you don't want
  them to have to write (or even think about) django templates. You have
  developers/designers that will develop your templates for CMS pages.
* You want a simple CMS app that is easy to configure, and for the most part
  just gets out of your way.


Setup
=====

#. Install turrentine. Pip is recommended and can be used as follows::

    pip install -e git://github.com/af/turrentine.git#egg=turrentine

#. Add 'turrentine' to your installed apps in settings.py::

    INSTALLED_APPS = (
        # Your other apps here
        'turrentine',
    )

#. Add turrentine at the **end** of your root urlconf::

    urlpatterns = patterns('',
        # Your other urls go here

        (r'^', include('turrentine.urls')),     # Make sure this is the last entry
    )

#. If you haven't already, you probably also want to enable django's dev static
   file serving in your `urls.py`. This will ensure that turrentine's admin css/js will work
   while in development::

        from django.contrib.staticfiles.urls import staticfiles_urlpatterns

        # ... the rest of your URLconf here ...

        urlpatterns += staticfiles_urlpatterns()

        # Again, make sure turrentine comes last, even after the staticfiles_urlpatterns:
        urlpatterns += patterns('',
            (r'^', include('turrentine.urls')),
        )

   More info and background on this can be found at
   https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-development-view

#. Run ``python manage.py syncdb`` to add turrentine's tables to your database.

#. Back in settings.py, define ``TURRENTINE_TEMPLATE_ROOT`` and ``TURRENTINE_TEMPLATE_SUBDIR``.
   The former is the directory on your filesystem where you keep most of your templates
   (generally this is $PROJECT_ROOT/templates). The latter is the subdirectory where you
   want to put templates that the cms can use.
   The following will probably work for your project::

    import os.path
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    TURRENTINE_TEMPLATE_ROOT = os.path.join(PROJECT_ROOT, 'templates')
    TURRENTINE_TEMPLATE_SUBDIR = os.path.join(TURRENTINE_TEMPLATE_ROOT, 'cms')

#. Create a directory for your CMS templates, corresponding to the setting you
   made in the previous step::

    mkdir -p templates/cms

#. Create template(s) in the ``TURRENTINE_TEMPLATE_SUBDIR`` directory, so they can be
   used by your pages. You'll probably want to use the following template variables
   (which are hopefully self-explanatory):

    - ``{{ page.title }}``
    - ``{{ page.content }}``
    - ``{{ page.meta_description }}``
    - ``{{ page.meta_keywords }}``


Adding Support for Versioned Content
------------------------------------

Out of the box, turrentine doesn't track revisions of your content. However, if
you'd like to enable version tracking, install the very nice `django-reversion
<https://github.com/etianen/django-reversion>`_ app. Once ``django-reversion`` is `installed and
configured <https://github.com/etianen/django-reversion/wiki>`_, you'll be able to access
previous versions of Turrentine CMS pages in the admin (using the "History" link in the
top right corner).


The Name
---------

In fine django tradition, turrentine is named after a jazz musician, the late
great tenor saxophonist Stanley Turrentine. Nicknamed "The Sugar Man",
Turrentine was famous for his bluesy feel and big sound. Check out his album
"Hustlin'", and his classic recordings with organist Jimmy Smith.
