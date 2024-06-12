from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.contrib.auth.decorators import login_required
from .models import Ingredient, UserIngredient, Foods, FoodToIngredient
from .forms import NewIngredientForm, AddUserIngredientForm
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def home(request):
    return render(request, 'food/home.html')

@login_required
def login(request):
    return render(request, "login.html")

class NewIngredientsForm(forms.Form):
    ingredients = forms.CharField(label="Ingredients")

@login_required
def ingredients(request):
    if request.method == "POST":
        user_ingredient_form = AddUserIngredientForm(request.POST)
        user_ingredient = user_ingredient_form.save(commit=False)
        user_ingredient.user = request.user
        user_ingredient.save()
        return redirect('food:ingredients')
    else:
        user_ingredient_form = AddUserIngredientForm()

    user_ingredients = UserIngredient.objects.filter(user=request.user)
    return render(request, "food/ingredients.html", {
        "ingredients": user_ingredients,
        "user_ingredient_form": user_ingredient_form
    })

@login_required
def food(request, id):
    food = Foods.objects.get(pk = id)
    return render(request, "food/food.html",{
        "food": food
    })

@login_required
def add(request):
    if request.method == "POST":
        ingredient_form = NewIngredientForm(request.POST)
        if ingredient_form.is_valid():
            ingredient = ingredient_form.save()
            UserIngredient.objects.create(user=request.user, ingredient=ingredient)
            return redirect('food:ingredients')
    else:
        ingredient_form = NewIngredientForm()
    return render(request, "food/add.html",{
        "ingredient_form": ingredient_form
    })

@login_required
def delete(request, id):
    if request.method == "POST":
        ingredient = UserIngredient.objects.get(pk = id, user = request.user)
        ingredient.delete()
    return redirect('food:ingredients')

@login_required
def nutrition(request, id):
    nutrition_value = Ingredient.objects.get(pk=id)
    return render(request, "food/nutrition.html",{
        "ingredient": nutrition_value
    })

