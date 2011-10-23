from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase

from turrentine.models import CMSPage, CMSPageManager

class ModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')

    def test_manager(self):
        # Test absolute url validation:
        self.assertRaises(ValidationError, CMSPageManager.ensure_absolute_url, 'asdf',)
        self.assertEqual(None, CMSPageManager.ensure_absolute_url('/asdf'))

        # Test the published() manager method:
        self.assertEqual(0, CMSPage.objects.published().count())
        CMSPage.objects.create(title='test page', url='/turr_test', is_published=False, author=self.user)
        self.assertEqual(0, CMSPage.objects.published().count())
        CMSPage.objects.create(title='test page', url='/turr_test2', is_published=True, author=self.user)
        self.assertEqual(1, CMSPage.objects.published().count())


class ViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='test')
        self.user.set_password('password'); self.user.save()
        self.url = '/turr_test/'
        self.page = CMSPage.objects.create(title='test page', url=self.url, is_published=True, author=self.user)

    def test_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_404_for_unpublished(self):
        self.page.is_published = False
        self.page.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

    def test_append_slash(self):
        # Ensure that APPEND_SLASH=True works for cms pages:
        settings.APPEND_SLASH = False
        response = self.client.get(self.url[:-1])
        self.assertEqual(response.status_code, 404)

        settings.APPEND_SLASH = True
        response = self.client.get(self.url[:-1])
        self.assertEqual(response.status_code, 301)
        self.assert_(dict(response.items())['Location'].endswith(self.url))

    def test_login_required(self):
        self.page.login_required = True
        self.page.save()

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assert_(dict(response.items())['Location'].find(settings.LOGIN_URL) != -1)

        self.client.login(username=self.user.username, password='password')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_staff_only(self):
        self.client.login(username=self.user.username, password='password')

        self.page.staff_only = True
        self.page.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)

        self.user.is_staff = True
        self.user.save()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
