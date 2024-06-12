from django.core.management import call_command
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Load all data (foods, ingredients, and food to ingredient relationships) from CSV files'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting to load all data...'))

        # Load foods
        self.stdout.write(self.style.SUCCESS('Loading foods...'))
        call_command('load_foods')
        self.stdout.write(self.style.SUCCESS('Foods loaded successfully.'))

        # Load ingredients
        self.stdout.write(self.style.SUCCESS('Loading ingredients...'))
        call_command('load_ingredients')
        self.stdout.write(self.style.SUCCESS('Ingredients loaded successfully.'))

        # Load food to ingredient relationships
        self.stdout.write(self.style.SUCCESS('Loading food to ingredient relationships...'))
        call_command('load_food_to_ingredients')
        self.stdout.write(self.style.SUCCESS('Food to ingredient relationships loaded successfully.'))

        self.stdout.write(self.style.SUCCESS('All data loaded successfully.'))
