from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django import forms
from django.contrib.auth.decorators import login_required
from .models import Ingredient, UserIngredient, Food, Nutrition
import pandas as pd
from .forms import IngredientForm, NutritionForm, AddUserIngredientForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import requests
from Levenshtein import distance
import re


def get_foods_for_ingredient(ingredient):
    # Check if foods for the ingredient already exist in the database
    ingredient_obj = Ingredient.objects.get(name=ingredient)
    foods = ingredient_obj.foods.all()

    if not foods:
        # If not, fetch from the API
        url = f"https://en.wikibooks.org/w/api.php"
        params = {
            'action': 'query',
            'list': 'search',
            'srsearch': f"Cookbook:{ingredient}",
            'format': 'json'
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            search_results = data.get('query', {}).get('search', [])
            for result in search_results:
                food_title = result['title']
                ingredient_name = Ingredient.objects.filter(name=food_title.split(':', 1)[1])
                if not ingredient_name:
                    food, created = Food.objects.get_or_create(title=food_title)
                    food.ingredients.add(ingredient_obj)
                    food.save()
            foods = ingredient_obj.foods.all()
        else:
            print(f"Failed to get data for ingredient: {ingredient}")
    
    return [food.title for food in foods]
    
def fetch_wikibook_content(title):
    url = "https://en.wikibooks.org/w/api.php"
    params = {
        'action': 'query',
        'prop': 'revisions',
        'titles': title,
        'rvprop': 'content',
        'format': 'json'
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        pages = data.get('query', {}).get('pages', {})
        page_id, page_info = next(iter(pages.items()))
        page_content = page_info.get('revisions', [{}])[0].get('*', '')
        
        # Handle redirects
        if '#REDIRECT' in page_content:
            redirect_target = page_content.split('[[', 1)[1].split(']]', 1)[0].strip()
            if not redirect_target.startswith('Cookbook:'):
                redirect_target = 'Cookbook:' + redirect_target
            return fetch_wikibook_content(redirect_target.replace(' ', '_'))
        
        return page_content
    else:
        return None

def extract_information(content):
    ingredients, procedures, notes = [], [], []
    
    # Normalize the content to ensure uniformity
    normalized_content = content.replace("==Ingredients==", "== Ingredients ==") \
                                .replace("==Procedure==", "== Procedure ==") \
                                .replace("==Notes, tips, and variations==", "== Notes, tips, and variations ==")
    
    # Extract the ingredients
    if "== Ingredients ==" in normalized_content:
        ingredients_section = normalized_content.split("== Ingredients ==")[1].split("== Procedure ==")[0]
        ingredients = parse_section(ingredients_section)
    
    # Extract the procedures
    if "== Procedure ==" in normalized_content:
        procedure_section = normalized_content.split("== Procedure ==")[1].split("== Notes")[0]
        procedures = parse_section(procedure_section)
    
    # Extract the notes
    if "== Notes, tips, and variations ==" in normalized_content:
        notes_section = normalized_content.split("== Notes, tips, and variations ==")[1]
        notes = []
        for line in notes_section.split('\n'):
            line = line.strip()
            if line.startswith('[[Category:') or line.startswith("=="):
                break  # Stop if a category starts
            if line:
                notes.append(line)
    
    return ingredients, procedures, notes

def parse_section(section):
    parsed_list = []
    current_sublist = []
    current_header = None

    in_table = False
    table_content = []
    headers = []

    for line in section.split('\n'):
        line = line.strip()
        if line.startswith('==='):
            if current_sublist:
                parsed_list.append(current_sublist)
                current_sublist = []
            current_header = line.replace('=', '').strip()
            current_sublist.append(f"= {current_header}")
        elif line.startswith('[[Category') or line.startswith('=='):
            break
        elif line.startswith('{| class="wikitable"'):
            in_table = True
        elif line.startswith('|}') and in_table:
            in_table = False
            if headers:
                table_content.insert(0, headers)
            current_sublist.append(format_table(table_content))
            table_content = []
            headers = []
        elif in_table:
            if line.startswith('!'):
                headers.append(line.replace('!', '').strip())
            elif line.startswith('|-'):
                table_content.append([])  # Initialize a new row
            elif line.startswith('|'):
                if not table_content:
                    table_content.append([])  # Ensure there's a row to append to
                table_content[-1].append(line.replace('|', '').strip())
        elif line:
            current_sublist.append(line)
    
    if current_sublist:
        parsed_list.append(current_sublist)
    
    return parsed_list

def format_table(table):
    formatted_table = []
    headers = table.pop(0)
    formatted_table.append(" | ".join(headers))
    for row in table:
        formatted_table.append(" | ".join(row))
    return "\n".join(formatted_table)

def search_ingredient_by_name(ingredient_name):
    matches = Nutrition.objects.filter(ingredient_description_first__icontains=ingredient_name)
    if not matches.exists():
        matches = Nutrition.objects.filter(ingredient_description_second__icontains=ingredient_name)
    if not matches.exists():
        matches = Nutrition.objects.filter(ingredient_description_third__icontains=ingredient_name)
    match_values = list(matches.values('pk', 'ingredient_description'))

    # Combine ids and descriptions into a list of dictionaries
    variations = [{'id': match['pk'], 'description': match['ingredient_description']} for match in match_values]
    
    print(variations)
    return variations

def fetch_nutritional_data(query):
    url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
    headers = {
        'x-app-id': "53a454b3",
        'x-app-key': "4371285aacc1cc0fbc6442107b2d1e8c",
        'Content-Type': 'application/json'
    }
    data = {
        'query': query
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        return None
    
def parse_and_sum_nutritionix_response(response):
    if 'foods' not in response:
        return {}

    total_nutrition_info = {
        'calories': 0,
        'total_fat': 0,
        'saturated_fat': 0,
        'cholesterol': 0,
        'sodium': 0,
        'total_carbohydrate': 0,
        'dietary_fiber': 0,
        'sugars': 0,
        'protein': 0,
        'potassium': 0,
        'phosphorus': 0
    }

    for food_data in response['foods']:
        total_nutrition_info['calories'] += food_data.get('nf_calories', 0) or 0
        total_nutrition_info['total_fat'] += food_data.get('nf_total_fat', 0) or 0
        total_nutrition_info['saturated_fat'] += food_data.get('nf_saturated_fat', 0) or 0
        total_nutrition_info['cholesterol'] += food_data.get('nf_cholesterol', 0) or 0
        total_nutrition_info['sodium'] += food_data.get('nf_sodium', 0) or 0
        total_nutrition_info['total_carbohydrate'] += food_data.get('nf_total_carbohydrate', 0) or 0
        total_nutrition_info['dietary_fiber'] += food_data.get('nf_dietary_fiber', 0) or 0
        total_nutrition_info['sugars'] += food_data.get('nf_sugars', 0) or 0
        total_nutrition_info['protein'] += food_data.get('nf_protein', 0) or 0
        total_nutrition_info['potassium'] += food_data.get('nf_potassium', 0) or 0
        total_nutrition_info['phosphorus'] += food_data.get('nf_p', 0) or 0

    for key in total_nutrition_info:
        total_nutrition_info[key] = round(total_nutrition_info[key], 2)

    return total_nutrition_info


# Create your views here.
@login_required
def home(request):
    return render(request, 'food/home.html')

"""
def find_nutritional_values(ingredient):
    for value in ingredient.split(','):
        result = nutrient_data[nutrient_data['Main food description'].str.contains(value.strip(), case=False, na=False)]
        if not result.empty:
            return result.to_dict(orient='records')
    return None



def search_nutritional_info(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, id=ingredient_id)
    nutritional_values = find_nutritional_values(ingredient.name)
    
    if request.method == 'POST':
        selected_value = request.POST.get('selected_value')
        if selected_value:
            selected_value = eval(selected_value)
            NutritionForm.objects.create(
                ingredient=ingredient,
                main_food_description=selected_value.get('Main food description'),
                calories=selected_value.get('Calories'),
                protein=selected_value.get('Protein'),
                fat=selected_value.get('Fat'),
                carbohydrates=selected_value.get('Carbohydrates')
            )
            return redirect('ingredient_list')
    
    context = {'ingredient': ingredient, 'nutritional_values': nutritional_values}
    return render(request, 'search_nutritional_info.html', context)

    def search_ingredient_by_name(ingredient_name, nutrient_data):
    # Split the ingredient name into parts separated by comma
    ingredient_parts = [part.strip() for part in ingredient_name.split(',')]
    
    # Iterate through each part to find matching ingredients
    for part in ingredient_parts:
        matches = nutrient_data[nutrient_data['ingredient_description'].str.contains(f"^{part}", case=False, na=False, regex=True)]
        if not matches.empty:
            return matches.drop_duplicates()  # Return the first match found and stop searching
    
    return pd.DataFrame()
"""


@login_required
def add(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)
        if form.is_valid():
            ingredient = form.save()

            return redirect('search_nutritional_info', ingredient_id=ingredient.id)
    else:
        form = IngredientForm()
    return render(request, 'add.html', {'form': form})

@login_required
def ingredients(request):
    all_ingredients = Ingredient.objects.all()
    user_ingredients = UserIngredient.objects.filter(user=request.user)

    if request.method == 'POST':
        ingredient_name = request.POST.get('name')

        # Check if the ingredient is already in user's ingredients
        if user_ingredients.filter(ingredient__name=ingredient_name).exists():
            return redirect('food:ingredients')  # Do nothing if it exists

        # Check if the ingredient is in all ingredients
        if all_ingredients.filter(name=ingredient_name).exists():
            ingredient = all_ingredients.get(name=ingredient_name)
            UserIngredient.objects.get_or_create(user=request.user, ingredient=ingredient)

        return redirect('food:ingredients')


    return render(request, "food/ingredients.html", {
        'ingredients': [
            {
                'ingredient': ui,
                'variations': search_ingredient_by_name(ui.ingredient.name),
            }
            for ui in user_ingredients
        ],
        'all_ingredients': all_ingredients,
    })




def foods(request):
    user_ingredients = UserIngredient.objects.filter(user=request.user)
    foods = []
    
    for user_ingredient in user_ingredients:
        food_titles = get_foods_for_ingredient(user_ingredient.ingredient.name)
        for food_title in food_titles:
            cleaned_food = food_title.replace("Cookbook:", "").replace("_", " ")
            if cleaned_food not in foods:
                foods.append(cleaned_food)
    
    return render(request, "food/foods.html", {
        "foods": foods
    })

@login_required
def delete(request, name):
    if request.method == "POST":
        id = Ingredient.objects.get(name = name)
        ingredient = UserIngredient.objects.get(ingredient = id, user = request.user)
        ingredient.delete()
    return redirect('food:ingredients')

def preprocess_ingredients(ingredients):
    cleaned_ingredients = []
    for sublist in ingredients:
        for item in sublist:
            if not item.startswith("="):
                cleaned_item = re.sub(r'\[\[.*?\|(.*?)\]\]', r'\1', item)  # Remove Wikibook formatting
                cleaned_item = cleaned_item.replace("*", "").strip()  # Remove '*' and extra spaces
                cleaned_ingredients.append(cleaned_item)
    return cleaned_ingredients


def replace_ranges_with_averages(ingredients):
    def calculate_average_with_unit(match):
        start, end, unit = match.groups()
        start, end = int(start), int(end)
        average = (start + end) // 2
        return f"{average} {unit}"

    def calculate_average_without_unit(match):
        start, end = match.groups()
        start, end = int(start), int(end)
        average = (start + end) // 2
        return str(average)

    # Patterns for ranges with and without units
    pattern_with_unit = re.compile(r'(\d+)\s*[-–]\s*(\d+)\s*(g)')
    pattern_without_unit = re.compile(r'(\d+)\s*[-–]\s*(\d+)\s*(?!g)')

    updated_ingredients = []
    for ingredient in ingredients:
        ingredient = pattern_with_unit.sub(calculate_average_with_unit, ingredient)
        ingredient = pattern_without_unit.sub(calculate_average_without_unit, ingredient)
        updated_ingredients.append(ingredient)

    return updated_ingredients

def food_item(request, name):
    title = f"Cookbook:{name.replace(' ', '_')}"
    content = fetch_wikibook_content(title)
    if content:
        ingredients, procedures, notes = extract_information(content)
        cleaned_ingredients = preprocess_ingredients(ingredients)
        cleaned_ingredients = replace_ranges_with_averages(cleaned_ingredients)
        cleaned_ingredients = "\n".join(cleaned_ingredients)
        nutritional_data = fetch_nutritional_data(cleaned_ingredients)
        nutritional_data = parse_and_sum_nutritionix_response(nutritional_data)
        return render(request, "food/food_item.html", {
            "name": name,
            "ingredients": ingredients,
            "procedures": procedures,
            "notes": notes,
            "nutritional_data": nutritional_data
        })
    else:
        return render(request, "food/food_item.html", {
            "name": name,
            "ingredients": [],
            "procedures": [],
            "notes": [],
            "nutritional_data": {}
        })

@login_required
def nutrition(request):
    if request.method == "POST":
        id = request.POST.get("ingredient_variation")
        nutrition_info = get_object_or_404(Nutrition, pk=id)
        
        # Render the nutrition information to a template
        return render(request, 'food/nutrition.html', {
            'nutrition_info': nutrition_info,
        })
    else:
        # Handle GET request if needed, otherwise, redirect or show an error
        return redirect('food:ingredients')
"""

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
def foods(request):
    # Get the ingredients that the current user has
    user_ingredients = UserIngredient.objects.filter(user=request.user).values_list('ingredient', flat=True)
    
    # Find all foods
    foods = Foods.objects.all()

    # Filter foods where all ingredients are in user's ingredients
    valid_foods = []
    for food in foods:
        food_ingredients = FoodToIngredient.objects.filter(food=food).values_list('ingredient', flat=True)
        if all(ingredient in user_ingredients for ingredient in food_ingredients):
            valid_foods.append(food)

    return render(request, "food/foods.html", {
        "foods": valid_foods
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




"""

