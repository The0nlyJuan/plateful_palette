from django import forms
from .models import Ingredient, UserIngredient

class NewIngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = '__all__'  # This will include all fields in the form

class AddUserIngredientForm(forms.ModelForm):
    class Meta:
        model = UserIngredient
        fields = ['ingredient']
