import requests

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

response = fetch_nutritional_data("Skin-on chicken legs, breasts, or wings (sufficient for the number of people you are cooking for) 1 tin (400 ml) coconut milk 1 lime, zested and juiced 1 bunch fresh mint, chopped 1 large sprinkle of paprika")
total_nutrition_info = parse_and_sum_nutritionix_response(response)
print(total_nutrition_info)

