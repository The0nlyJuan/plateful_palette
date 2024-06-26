from django.contrib.auth.models import User
from django.db import models

class Nutrition(models.Model):
    ingredient_code = models.IntegerField(primary_key=True)
    ingredient_description = models.CharField(max_length=255)
    alcohol = models.FloatField(null=True, blank=True)
    caffeine = models.FloatField(null=True, blank=True)
    calcium = models.FloatField(null=True, blank=True)
    carbohydrate = models.FloatField(null=True, blank=True)
    carotene_alpha = models.FloatField(null=True, blank=True)
    carotene_beta = models.FloatField(null=True, blank=True)
    cholesterol = models.FloatField(null=True, blank=True)
    choline_total = models.FloatField(null=True, blank=True)
    copper = models.FloatField(null=True, blank=True)
    cryptoxanthin_beta = models.FloatField(null=True, blank=True)
    energy = models.FloatField(null=True, blank=True)
    fatty_acids_total_monounsaturated = models.FloatField(null=True, blank=True)
    fatty_acids_total_polyunsaturated = models.FloatField(null=True, blank=True)
    fatty_acids_total_saturated = models.FloatField(null=True, blank=True)
    fiber_total_dietary = models.FloatField(null=True, blank=True)
    folate_DFE = models.FloatField(null=True, blank=True)
    folate_food = models.FloatField(null=True, blank=True)
    folate_total = models.FloatField(null=True, blank=True)
    folic_acid = models.FloatField(null=True, blank=True)
    iron = models.FloatField(null=True, blank=True)
    lutein_zeaxanthin = models.FloatField(null=True, blank=True)
    lycopene = models.FloatField(null=True, blank=True)
    magnesium = models.FloatField(null=True, blank=True)
    niacin = models.FloatField(null=True, blank=True)
    phosphorus = models.FloatField(null=True, blank=True)
    potassium = models.FloatField(null=True, blank=True)
    protein = models.FloatField(null=True, blank=True)
    retinol = models.FloatField(null=True, blank=True)
    riboflavin = models.FloatField(null=True, blank=True)
    selenium = models.FloatField(null=True, blank=True)
    sodium = models.FloatField(null=True, blank=True)
    sugars_total = models.FloatField(null=True, blank=True)
    theobromine = models.FloatField(null=True, blank=True)
    thiamin = models.FloatField(null=True, blank=True)
    total_fat = models.FloatField(null=True, blank=True)
    vitamin_A_RAE = models.FloatField(null=True, blank=True)
    vitamin_B12 = models.FloatField(null=True, blank=True)
    vitamin_B12_added = models.FloatField(null=True, blank=True)
    vitamin_B6 = models.FloatField(null=True, blank=True)
    vitamin_C = models.FloatField(null=True, blank=True)
    vitamin_D_D2_D3 = models.FloatField(null=True, blank=True)
    vitamin_E_alpha_tocopherol = models.FloatField(null=True, blank=True)
    vitamin_E_added = models.FloatField(null=True, blank=True)
    vitamin_K_phylloquinone = models.FloatField(null=True, blank=True)
    water = models.FloatField(null=True, blank=True)
    zinc = models.FloatField(null=True, blank=True)
    fatty_acid_10_0 = models.FloatField(null=True, blank=True)  # 10:0
    fatty_acid_12_0 = models.FloatField(null=True, blank=True)  # 12:0
    fatty_acid_14_0 = models.FloatField(null=True, blank=True)  # 14:0
    fatty_acid_16_0 = models.FloatField(null=True, blank=True)  # 16:0
    fatty_acid_16_1 = models.FloatField(null=True, blank=True)  # 16:1
    fatty_acid_18_0 = models.FloatField(null=True, blank=True)  # 18:0
    fatty_acid_18_1 = models.FloatField(null=True, blank=True)  # 18:1
    fatty_acid_18_2 = models.FloatField(null=True, blank=True)  # 18:2
    fatty_acid_18_3 = models.FloatField(null=True, blank=True)  # 18:3
    fatty_acid_18_4 = models.FloatField(null=True, blank=True)  # 18:4
    fatty_acid_20_1 = models.FloatField(null=True, blank=True)  # 20:1
    fatty_acid_20_4 = models.FloatField(null=True, blank=True)  # 20:4
    fatty_acid_20_5_n3 = models.FloatField(null=True, blank=True)  # 20:5 n-3
    fatty_acid_22_1 = models.FloatField(null=True, blank=True)  # 22:1
    fatty_acid_22_5_n3 = models.FloatField(null=True, blank=True)  # 22:5 n-3
    fatty_acid_22_6_n3 = models.FloatField(null=True, blank=True)  # 22:6 n-3
    fatty_acid_4_0 = models.FloatField(null=True, blank=True)  # 4:0
    fatty_acid_6_0 = models.FloatField(null=True, blank=True)  # 6:0
    fatty_acid_8_0 = models.FloatField(null=True, blank=True)  # 8:0

    def __str__(self):
        return self.ingredient_description

class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class UserIngredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    # Add any additional fields here, e.g., quantity

    class Meta:
        unique_together = ('user', 'ingredient')  # Ensures each user can only have each ingredient once

    def __str__(self):
        return f"{self.user.username} - {self.ingredient.ingredient_description}"
    
class Food(models.Model):
    title = models.CharField(max_length=255)
    ingredients = models.ManyToManyField('Ingredient', related_name='foods')

    def __str__(self):
        return self.title

class UserFood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.food.title}"


