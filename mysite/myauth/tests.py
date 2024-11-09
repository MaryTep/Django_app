from django.test import TestCase
from django.urls import reverse


class GetCookieViewTestCase(TestCase):
    def test_get_cookie_view(self):
        response = self.client.get(reverse("myauth:get_cookie"), HTTP_USER_AGENT="Mozilla/5.0")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Cookie value")


class FooBarViewTestCase(TestCase):
    def test_foo_bar_view(self):
        response = self.client.get(reverse("myauth:foo_bar"), HTTP_USER_AGENT="Mozilla/5.0")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['content-type'], 'application/json')
        expected_data = {"foo": "bar", "spam": "eggs"}
        self.assertJSONEqual(response.content, expected_data)