from django.test import TestCase
from django.urls import reverse
from .models import Ingredient, Food
from django.contrib.auth import get_user_model

User = get_user_model()

class FoodTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_add_ingredient(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('food:add'), {'name': 'Tomato'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ingredient.objects.filter(name='Tomato').exists())

    def test_view_food(self):
        self.client.login(username='testuser', password='password123')
        ingredient = Ingredient.objects.create(name='Tomato')
        food = Food.objects.create(title='Tomato Soup')
        food.ingredients.add(ingredient)
        food.save()

        response = self.client.get(reverse('food:foods'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Tomato Soup')

# Create your tests here.
