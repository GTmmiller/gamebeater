from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.contrib.auth.models import AnonymousUser, User

from .views import DashboardView
from .models import GamebeaterProfile

class DasboardViewTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_dashboard_with_anonymous_user(self):
        request = self.factory.get(reverse("profiles:dashboard"))
        request.user = AnonymousUser()
 
        response = DashboardView.as_view()(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login") + "?next=" + reverse("profiles:dashboard"))

    def test_dashboard_with_no_games_user(self):
        regular_user = User.objects.create_user(
            username='mock_user',
            email='mock@email.com',
            password='secret'
        )
        GamebeaterProfile.objects.create(user=regular_user)

        request = self.factory.get(reverse("profiles:dashboard"))
        request.user = regular_user

        response = DashboardView.as_view()(request)
        self.assertEqual(response.status_code, 200)
        
        