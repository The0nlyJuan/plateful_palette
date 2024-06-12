import csv
from django.core.management.base import BaseCommand
from food.models import Foods  # Replace 'food' with the actual app name

class Command(BaseCommand):
    help = 'Load foods from CSV file into food_foods table'

    def handle(self, *args, **kwargs):
        with open("foods.csv", 'r') as file:  # Replace with the actual path to your CSV file
            reader = csv.DictReader(file)
            for row in reader:
                # Replace problematic characters
                for key in row:
                    if row[key]:
                        row[key] = row[key].replace('�', "'")
                        row[key] = row[key].replace('�', "'")

                Foods.objects.update_or_create(
                    food_code=row['Food code'],
                    defaults={
                        'food_description': row['Main food description'],
                        'food_additional_description': row.get('Food_additional_description', None)
                    }
                )
        self.stdout.write(self.style.SUCCESS('Successfully loaded foods'))
