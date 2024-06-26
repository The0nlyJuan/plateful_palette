import requests
from django.core.management.base import BaseCommand
from food.models import Ingredient  # Make sure to replace 'your_app' with your actual app name

class Command(BaseCommand):
    help = 'Fetch ingredients from Wikibooks and save them to the database'

    def fetch_all_ingredients(self):
        endpoint = "https://en.wikibooks.org/w/api.php"
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": "Category:Ingredients",
            "cmlimit": 500,
            "format": "json"
        }
        
        all_ingredients = []
        continue_token = None
        
        while True:
            if continue_token:
                params['cmcontinue'] = continue_token
            
            response = requests.get(endpoint, params=params)
            
            if response.status_code != 200:
                print("Error:", response.status_code)
                break
            
            data = response.json()
            all_ingredients.extend(member['title'] for member in data['query']['categorymembers'])
            
            if 'continue' in data:
                continue_token = data['continue']['cmcontinue']
            else:
                break

        return all_ingredients

    def handle(self, *args, **kwargs):
        ingredients = self.fetch_all_ingredients()
        for ingredient_name in ingredients:
            ingredient_name = ingredient_name.replace('Cookbook:', '').strip()
            Ingredient.objects.get_or_create(name=ingredient_name)
        self.stdout.write(self.style.SUCCESS('Successfully fetched and saved all ingredients'))
