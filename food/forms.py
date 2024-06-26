from django import forms
from .models import Ingredient, Nutrition, UserIngredient

"""
class NewIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'  # This will include all fields in the form
        """

class AddUserIngredientForm(forms.Form):
    ingredient_name = forms.CharField(max_length=255, label='Ingredient Name')

class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name']

class NutritionForm(forms.ModelForm):
    class Meta:
        model = Nutrition
        fields = '__all__'
