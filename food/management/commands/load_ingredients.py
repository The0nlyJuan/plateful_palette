import csv
from django.core.management.base import BaseCommand
from food.models import Ingredient  # Replace 'food' with the actual app name

class Command(BaseCommand):
    help = 'Load ingredients from CSV file'

    def handle(self, *args, **kwargs):
        with open("D:/Orbital/plateful_palette/ingredients.csv", 'r') as file:  # Replace with the actual path to your CSV file
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    Ingredient.objects.create(
                        ingredient_code=row['ingredient_code'],
                        ingredient_description=row['ingredient_description'],
                        alcohol=row['Alcohol'] or None,
                        caffeine=row['Caffeine'] or None,
                        calcium=row['Calcium'] or None,
                        carbohydrate=row['Carbohydrate'] or None,
                        carotene_alpha=row['Carotene, alpha'] or None,
                        carotene_beta=row['Carotene, beta'] or None,
                        cholesterol=row['Cholesterol'] or None,
                        choline_total=row['Choline, total'] or None,
                        copper=row['Copper'] or None,
                        cryptoxanthin_beta=row['Cryptoxanthin, beta'] or None,
                        energy=row['Energy'] or None,
                        fatty_acids_total_monounsaturated=row['Fatty acids, total monounsaturated'] or None,
                        fatty_acids_total_polyunsaturated=row['Fatty acids, total polyunsaturated'] or None,
                        fatty_acids_total_saturated=row['Fatty acids, total saturated'] or None,
                        fiber_total_dietary=row['Fiber, total dietary'] or None,
                        folate_DFE=row['Folate, DFE'] or None,
                        folate_food=row['Folate, food'] or None,
                        folate_total=row['Folate, total'] or None,
                        folic_acid=row['Folic acid'] or None,
                        iron=row['Iron'] or None,
                        lutein_zeaxanthin=row['Lutein + zeaxanthin'] or None,
                        lycopene=row['Lycopene'] or None,
                        magnesium=row['Magnesium'] or None,
                        niacin=row['Niacin'] or None,
                        phosphorus=row['Phosphorus'] or None,
                        potassium=row['Potassium'] or None,
                        protein=row['Protein'] or None,
                        retinol=row['Retinol'] or None,
                        riboflavin=row['Riboflavin'] or None,
                        selenium=row['Selenium'] or None,
                        sodium=row['Sodium'] or None,
                        sugars_total=row['Sugars, total'] or None,
                        theobromine=row['Theobromine'] or None,
                        thiamin=row['Thiamin'] or None,
                        total_fat=row['Total Fat'] or None,
                        vitamin_A_RAE=row['Vitamin A, RAE'] or None,
                        vitamin_B12=row['Vitamin B12'] or None,
                        vitamin_B12_added=row['Vitamin B12, added'] or None,
                        vitamin_B6=row['Vitamin B6'] or None,
                        vitamin_C=row['Vitamin C'] or None,
                        vitamin_D_D2_D3=row['Vitamin D (D2 + D3)'] or None,
                        vitamin_E_alpha_tocopherol=row['Vitamin E (alpha-tocopherol)'] or None,
                        vitamin_E_added=row['Vitamin E, added'] or None,
                        vitamin_K_phylloquinone=row['Vitamin K (phylloquinone)'] or None,
                        water=row['Water'] or None,
                        zinc=row['Zinc'] or None,
                        fatty_acid_10_0=row['10:0'] or None,
                        fatty_acid_12_0=row['12:0'] or None,
                        fatty_acid_14_0=row['14:0'] or None,
                        fatty_acid_16_0=row['16:0'] or None,
                        fatty_acid_16_1=row['16:1'] or None,
                        fatty_acid_18_0=row['18:0'] or None,
                        fatty_acid_18_1=row['18:1'] or None,
                        fatty_acid_18_2=row['18:2'] or None,
                        fatty_acid_18_3=row['18:3'] or None,
                        fatty_acid_18_4=row['18:4'] or None,
                        fatty_acid_20_1=row['20:1'] or None,
                        fatty_acid_20_4=row['20:4'] or None,
                        fatty_acid_20_5_n3=row['20:5 n-3'] or None,
                        fatty_acid_22_1=row['22:1'] or None,
                        fatty_acid_22_5_n3=row['22:5 n-3'] or None,
                        fatty_acid_22_6_n3=row['22:6 n-3'] or None,
                        fatty_acid_4_0=row['4:0'] or None,
                        fatty_acid_6_0=row['6:0'] or None,
                        fatty_acid_8_0=row['8:0'] or None,
                    )
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Skipping duplicate ingredient_code {row['ingredient_code']}: {str(e)}"))
        self.stdout.write(self.style.SUCCESS('Successfully loaded ingredients'))
