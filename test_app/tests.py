from django.test import Client, SimpleTestCase


class SimpleTest(SimpleTestCase):
    def setUp(self):
        self.client = Client()
        self.response = self.client.get('')

    def test_response(self):
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        self.assertTemplateUsed(self.response, 'main.html')
