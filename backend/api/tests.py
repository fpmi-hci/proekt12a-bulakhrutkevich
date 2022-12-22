from django.test import TestCase
from recipes.models import Ingredient
from django.test import SimpleTestCase
from django.urls import reverse


class IngredientTestCase(TestCase):
    def setUp(self):
        Ingredient.objects.create(name="a", measurement_unit="a")
        Ingredient.objects.create(name="b", measurement_unit="b")

    def test_measurments(self):
        lion = Ingredient.objects.get(name="a")
        cat = Ingredient.objects.get(name="b")
        self.assertEqual(lion.measurement_unit, 'a')
        self.assertEqual(cat.measurement_unit, 'b')


class UrlTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/api/recipes")
        self.assertEqual(response.status_code, 301)

    def test_url_exists_at_correct_location2(self):
        response = self.client.get("/admin")
        self.assertEqual(response.status_code, 301)

    def test_url_exists_at_correct_location3(self):
        response = self.client.get("api/auth")
        self.assertEqual(response.status_code, 404)

    def test_url_exists_at_correct_location4(self):
        response = self.client.get("/admin")
        self.assertEqual(response.status_code, 301)

    def test_url_exists_at_correct_location5(self):
        response = self.client.get("api/auth")
        self.assertEqual(response.status_code, 404)

    def test_url_exists_at_correct_location6(self):
        response = self.client.get("/admin")
        self.assertEqual(response.status_code, 301)

    def test_url_exists_at_correct_location7(self):
        response = self.client.get("api/auth")
        self.assertEqual(response.status_code, 404)

    def test_url_exists_at_correct_location8(self):
        response = self.client.get("/admin")
        self.assertEqual(response.status_code, 301)

    def test_url_exists_at_correct_location9(self):
        response = self.client.get("api/auth")
        self.assertEqual(response.status_code, 404)