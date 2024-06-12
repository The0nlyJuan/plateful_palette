import csv
from django.core.management.base import BaseCommand
from food.models import Foods, Ingredient, FoodToIngredient

class Command(BaseCommand):
    help = 'Load food to ingredient relationships from CSV file'

    def handle(self, *args, **kwargs):
        with open("D:/Orbital/plateful_palette/food_to_ingredients.csv", 'r', encoding='ISO-8859-1') as file:  # Replace with the actual path to your CSV file
            reader = csv.DictReader(file)
            for row in reader:
                food, created = Foods.objects.get_or_create(
                    food_code=row['Food code'],
                    defaults={'food_description': row['Main food description']}
                )
                ingredient, created = Ingredient.objects.get_or_create(
                    ingredient_code=row['Ingredient code'],
                    defaults={'ingredient_description': 'Unknown'}
                )
                FoodToIngredient.objects.update_or_create(
                    food=food,
                    ingredient=ingredient,
                    seq_num=row['Seq num'],
                    defaults={
                        'ingredient_weight': row['Ingredient weight (g)']
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded food to ingredient relationships'))
