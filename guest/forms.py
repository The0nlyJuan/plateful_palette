from django import forms
from food.models import UserIngredient

class AddUserIngredientForm(forms.ModelForm):
    class Meta:
        model = UserIngredient
        fields = ['ingredient']
