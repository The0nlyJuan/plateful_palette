from django.shortcuts import render, redirect
from django.http import HttpResponse
from django import forms
from django.contrib.auth.decorators import login_required
from .models import Ingredient, UserIngredient
from .forms import NewIngredientForm, AddUserIngredientForm

# Create your views here.

def home(request):
    return render(request, 'food/home.html')


def login(request):
    return render(request, "login.html")

class NewIngredientsForm(forms.Form):
    ingredients = forms.CharField(label="Ingredients")


def ingredients(request):
    if request.method == "POST":
        user_ingredient_form = AddUserIngredientForm(request.POST)
        user_ingredient = user_ingredient_form.save(commit=False)
        user_ingredient.user = request.user
        user_ingredient.save()
        return redirect('ingredients')
    else:
        user_ingredient_form = AddUserIngredientForm()

    user_ingredients = UserIngredient.objects.filter(user=request.user)
    return render(request, "food/ingredients.html", {
        "ingredients": user_ingredients,
        "user_ingredient_form": user_ingredient_form
    })

def food(request):
    return render(request, "food/food.html")

def suggestions(request):
    return render(request, "suggestions.html")

def recipe(request):
    return render(request, "recipe.html")

def add(request):
    if request.method == "POST":
        ingredient_form = NewIngredientForm(request.POST)
        if ingredient_form.is_valid():
            ingredient = ingredient_form.save()
            UserIngredient.objects.create(user=request.user, ingredient=ingredient)
            return redirect('ingredients')
    else:
        ingredient_form = NewIngredientForm()
    return render(request, "food/add.html",{
        "ingredient_form": ingredient_form,
    })