import csv
from django.core.management.base import BaseCommand
from food.models import Ingredient  # Replace 'myapp' with the actual app name

class Command(BaseCommand):
    help = 'Load ingredients from CSV file'

    def handle(self, *args, **kwargs):
        with open("D:\Orbital\plateful_palette\ingredients.csv", 'r') as file:  # Replace with the actual path to your CSV file
            reader = csv.DictReader(file)
            for row in reader:
                Ingredient.objects.create(
                    category=row['Category'],
                    description=row['Description'],
                    nutrient_data_bank_number=row['Nutrient Data Bank Number'],
                    data_alpha_carotene=row['Data.Alpha Carotene'] or None,
                    data_beta_carotene=row['Data.Beta Carotene'] or None,
                    data_beta_cryptoxanthin=row['Data.Beta Cryptoxanthin'] or None,
                    data_carbohydrate=row['Data.Carbohydrate'] or None,
                    data_cholesterol=row['Data.Cholesterol'] or None,
                    data_choline=row['Data.Choline'] or None,
                    data_fiber=row['Data.Fiber'] or None,
                    data_lutein_and_zeaxanthin=row['Data.Lutein and Zeaxanthin'] or None,
                    data_lycopene=row['Data.Lycopene'] or None,
                    data_niacin=row['Data.Niacin'] or None,
                    data_protein=row['Data.Protein'] or None,
                    data_retinol=row['Data.Retinol'] or None,
                    data_riboflavin=row['Data.Riboflavin'] or None,
                    data_selenium=row['Data.Selenium'] or None,
                    data_sugar_total=row['Data.Sugar Total'] or None,
                    data_thiamin=row['Data.Thiamin'] or None,
                    data_water=row['Data.Water'] or None,
                    data_fat_monosaturated_fat=row['Data.Fat.Monosaturated Fat'] or None,
                    data_fat_polysaturated_fat=row['Data.Fat.Polysaturated Fat'] or None,
                    data_fat_saturated_fat=row['Data.Fat.Saturated Fat'] or None,
                    data_fat_total_lipid=row['Data.Fat.Total Lipid'] or None,
                    data_major_minerals_calcium=row['Data.Major Minerals.Calcium'] or None,
                    data_major_minerals_copper=row['Data.Major Minerals.Copper'] or None,
                    data_major_minerals_iron=row['Data.Major Minerals.Iron'] or None,
                    data_major_minerals_magnesium=row['Data.Major Minerals.Magnesium'] or None,
                    data_major_minerals_phosphorus=row['Data.Major Minerals.Phosphorus'] or None,
                    data_major_minerals_potassium=row['Data.Major Minerals.Potassium'] or None,
                    data_major_minerals_sodium=row['Data.Major Minerals.Sodium'] or None,
                    data_major_minerals_zinc=row['Data.Major Minerals.Zinc'] or None,
                    data_vitamins_vitamin_a_rae=row['Data.Vitamins.Vitamin A - RAE'] or None,
                    data_vitamins_vitamin_b12=row['Data.Vitamins.Vitamin B12'] or None,
                    data_vitamins_vitamin_b6=row['Data.Vitamins.Vitamin B6'] or None,
                    data_vitamins_vitamin_c=row['Data.Vitamins.Vitamin C'] or None,
                    data_vitamins_vitamin_e=row['Data.Vitamins.Vitamin E'] or None,
                    data_vitamins_vitamin_k=row['Data.Vitamins.Vitamin K'] or None,
                )
