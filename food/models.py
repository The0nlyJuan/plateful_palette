from django.contrib.auth.models import User
from django.db import models

class Ingredient(models.Model):
    category = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    nutrient_data_bank_number = models.IntegerField()
    data_alpha_carotene = models.IntegerField(null=True, blank=True)  # micrograms (mcg)
    data_beta_carotene = models.IntegerField(null=True, blank=True)   # micrograms (mcg)
    data_beta_cryptoxanthin = models.IntegerField(null=True, blank=True)  # micrograms (mcg)
    data_carbohydrate = models.FloatField(null=True, blank=True)  # grams (g)
    data_cholesterol = models.IntegerField(null=True, blank=True)  # milligrams (mg)
    data_choline = models.FloatField(null=True, blank=True)  # milligrams (mg)
    data_fiber = models.FloatField(null=True, blank=True)  # grams (g)
    data_lutein_and_zeaxanthin = models.IntegerField(null=True, blank=True)  # micrograms (mcg)
    data_lycopene = models.IntegerField(null=True, blank=True)  # micrograms (mcg)
    data_niacin = models.FloatField(null=True, blank=True)  # milligrams (mg)
    data_protein = models.FloatField(null=True, blank=True)  # grams (g)
    data_retinol = models.IntegerField(null=True, blank=True)  # micrograms (mcg)
    data_riboflavin = models.FloatField(null=True, blank=True)  # milligrams (mg)
    data_selenium = models.FloatField(null=True, blank=True)  # micrograms (mcg)
    data_sugar_total = models.FloatField(null=True, blank=True)  # grams (g)
    data_thiamin = models.FloatField(null=True, blank=True)  # milligrams (mg)
    data_water = models.FloatField(null=True, blank=True)  # grams (g)
    data_fat_monosaturated_fat = models.FloatField(null=True, blank=True)  # grams (g)
    data_fat_polysaturated_fat = models.FloatField(null=True, blank=True)  # grams (g)
    data_fat_saturated_fat = models.FloatField(null=True, blank=True)  # grams (g)
    data_fat_total_lipid = models.FloatField(null=True, blank=True)  # grams (g)
    data_major_minerals_calcium = models.IntegerField(null=True, blank=True)  # milligrams (mg)
    data_major_minerals_copper = models.FloatField(null=True, blank=True)  # milligrams (mg)
    data_major_minerals_iron = models.FloatField(null=True, blank=True)  # milligrams (mg)
    data_major_minerals_magnesium = models.IntegerField(null=True, blank=True)  # milligrams (mg)
    data_major_minerals_phosphorus = models.IntegerField(null=True, blank=True)  # milligrams (mg)
    data_major_minerals_potassium = models.IntegerField(null=True, blank=True)  # milligrams (mg)
    data_major_minerals_sodium = models.IntegerField(null=True, blank=True)  # milligrams (mg)
    data_major_minerals_zinc = models.FloatField(null=True, blank=True)  # milligrams (mg)
    data_vitamins_vitamin_a_rae = models.IntegerField(null=True, blank=True)  # micrograms (mcg)
    data_vitamins_vitamin_b12 = models.FloatField(null=True, blank=True)  # micrograms (mcg)
    data_vitamins_vitamin_b6 = models.FloatField(null=True, blank=True)  # milligrams (mg)
    data_vitamins_vitamin_c = models.FloatField(null=True, blank=True)  # milligrams (mg)
    data_vitamins_vitamin_e = models.FloatField(null=True, blank=True)  # milligrams (mg)
    data_vitamins_vitamin_k = models.FloatField(null=True, blank=True)  # micrograms (mcg)

    def __str__(self):
        return self.description


    def __str__(self):
        return self.description


class UserIngredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    # Add any additional fields here, e.g., quantity

    class Meta:
        unique_together = ('user', 'ingredient')  # Ensures each user can only have each ingredient once

    def __str__(self):
        return f"{self.user.username} - {self.ingredient.name}"
