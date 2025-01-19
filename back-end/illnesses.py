import requests
import random

def main_illnesses():
    illnesses = {
        'Stroke': ['beef brisket', 'ham', 'bacon', 'ground pork', 'minced beef', 'beef', 'chorizo', 'lamb kidney', 
                   'lamb', 'pork', 'kielbasa', 'sausages', 'butter', 'whole milk', 'heavy cream', 'frying oil', 'dash vegetable oil'],
        'Heart Disease': ['beef brisket', 'ham', 'ground pork', 'bacon', 'minced beef', 'beef', 'chorizo', 'lamb kidney', 
                          'lamb', 'pork', 'kielbasa', 'sausages', 'butter', 'whole milk', 'heavy cream', 'double cream', 
                          'frying oil', 'dash vegetable oil'],
        'Diabetes': ['sugar', 'golden syrup', 'brown sugar', 'spaghetti', 'penne', 'basmati rice', 'sushi rice', 
                     'rice', 'white rice', 'flour'],
        'Acid Reflux/Ulcers': ['lemon', 'harissa spice', 'chilli powder', 'red chilli powder', 'madras paste', 'dried chilli powder', 
                                'vinegar', 'cayenne pepper', 'cajun', 'salsa', 'Allspice', 'scotch bonnet', 'soy sauce', 'dash hotsauce', 
                                'lemon juice', 'topping hotsauce', 'rice vinegar', 'jalapeno', 'green salsa', 'sliced and seeded jalapeno', 
                                'cooking wine', 'tomatoes', 'tomato puree', 'finely chopped tomatoes', 'garam masala', 'small cut chunks tomatoes', 
                                'finely sliced red onions', 'red wine vinegar', 'onion', 'garlic', 'dark soy sauce', 'dry white wine', 
                                'thai green curry paste', 'lime', 'mustard', 'apple cider vinegar', 'orange', 'balsamic vinegar', 
                                'tomato ketchup', 'tomato sauce', 'red wine', 'pickle juice']
    }
    return illnesses

def avoid_meals(main_ingredients_avoid):
    filter_url = "https://www.themealdb.com/api/json/v1/1/filter.php?i="
    avoiding_meals = {}

    for ingredient in main_ingredients_avoid:
        main_url = filter_url + ingredient
        try:
            response = requests.get(main_url).json()
            if response and response['meals']:
                meal_names = [meal['strMeal'] for meal in response['meals']]
                avoiding_meals[ingredient] = meal_names
        except Exception as e:
            print(f"Error fetching meals for ingredient '{ingredient}': {e}")
            continue

    return avoiding_meals

def get_all_meals():
    search_url = "https://www.themealdb.com/api/json/v1/1/search.php?f="
    all_meals = []
    letters = 'abcdefghijklmnopqrstuvwxyz'

    for letter in letters:
        try:
            response = requests.get(search_url + letter).json()
            if response and response['meals']:
                meals = [meal['strMeal'] for meal in response['meals']]
                all_meals.extend(meals)
        except Exception as e:
            print(f"Error fetching meals starting with '{letter}': {e}")
            continue

    return all_meals

def filter_meals(all_meals, meals_to_avoid):
    avoided_set = set(meal for meals in meals_to_avoid.values() for meal in meals)
    return [meal for meal in all_meals if meal not in avoided_set]

def get_recipe(meal_id):
    """Fetch and display the recipe for a specific meal ID."""
    recipe_url = f"https://www.themealdb.com/api/json/v1/1/lookup.php?i={meal_id}"
    try:
        response = requests.get(recipe_url)
        if response.status_code == 200:
            meal = response.json()["meals"][0]
            print("\nRecipe Details:")
            print(f"- Name: {meal['strMeal']}")
            print(f"- Category: {meal['strCategory']}")
            print(f"- Area: {meal['strArea']}")
            print(f"- Instructions:\n{meal['strInstructions']}")
            print(f"- Ingredients:")
            
            for i in range(1, 21):  
                ingredient = meal.get(f"strIngredient{i}")
                measure = meal.get(f"strMeasure{i}")
                if ingredient and ingredient.strip():
                    print(f"  - {ingredient} ({measure.strip() if measure else 'to taste'})")
        else:
            print(f"Failed to fetch the recipe. Status Code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while fetching the recipe: {e}")

def get_meal_ids(meal_names):
    """Fetch the meal IDs for given meal names."""
    meal_ids = []
    for meal_name in meal_names:
        try:
            search_url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal_name}"
            response = requests.get(search_url).json()
            if response['meals']:
                meal_ids.append(response['meals'][0]['idMeal'])
        except Exception as e:
            print(f"Error fetching meal ID for {meal_name}: {e}")
    return meal_ids

def generate_recipes(filtered_meals, meal_count, meal_type):
    """Fetch and display random recipes for the filtered meals."""
    print(f"\n{meal_type} Recipes:")
    random_meals = random.sample(filtered_meals, min(meal_count, len(filtered_meals)))
    meal_ids = get_meal_ids(random_meals)
    for meal_id in meal_ids:
        get_recipe(meal_id)

if __name__ == "__main__":
    illnesses = main_illnesses()
    for illness, ingredients_to_avoid in illnesses.items():
        print(f"\nIllness: {illness}")
        print("Avoiding ingredients:", ", ".join(ingredients_to_avoid))
        meals_to_avoid = avoid_meals(ingredients_to_avoid)

        all_meals = get_all_meals()
        allowed_meals = filter_meals(all_meals, meals_to_avoid)

        generate_recipes(allowed_meals, 3, "Breakfast")
        generate_recipes(allowed_meals, 6, "Lunch/Dinner")
