import requests
import random
from fastapi import FastAPI
from pydantic import BaseModel


def healthy_lifestyle(type_diet):
    main_ingredients = []
    if type_diet == 'carnivore diet':
        main_ingredients = ['Chicken Breasts', 'Lamb', 'Beef Fillet', 'Parma Ham', 'Beef', 'Beef Stock', 'Bacon', 'Chicken', 'Pork', 'Chicken Stock' ]
    elif type_diet == 'pescatarian':
        main_ingredients = ['Salmon', 'Prawns', 'clams', 'oysters', 'mussels', 'Raw King Prawns', 'Monkfish']
    else:
        type_diet == 'vegetarian'
        main_ingredients = ['Chicken Breasts', 'Lamb', 'Beef Fillet', 'Parma Ham', 'Beef', 'Beef Stock', 'Bacon', 'Chicken', 'Pork', 'Chicken Stock',
                            'Salmon', 'Prawns', 'clams', 'oysters', 'mussels', 'Raw King Prawns', 'Monkfish']

    return main_ingredients

def get_all_meals():
    search_url = "https://www.themealdb.com/api/json/v1/1/search.php?f="
    all_meals = []
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    
    for letter in letters:
        response = requests.get(search_url + letter).json()
    
        if response and response['meals']:
            meals = [meal['strMeal'] for meal in response['meals']]
            all_meals.extend(meals)
    
    return all_meals


def filter_meals(avoid_needed_ingrediants):
    filter_url = "https://www.themealdb.com/api/json/v1/1/filter.php?i="
    avoiding_meals = []
    
    for ingredient in avoid_needed_ingrediants:
        main_url = filter_url + ingredient
        response = requests.get(main_url).json()
        
        if 'meals' in response and response['meals']:  
            meal_names = [meal['strMeal'] for meal in response['meals']]
            avoiding_meals.update(meal_names) 
    
    return list(avoiding_meals)

def vegeterian(avoid_meals):
    all_meals = get_all_meals()
    return [meal for meal in all_meals if meal not in avoid_meals]

def carnivore_pescatarian(needed_meals):
    all_meals = get_all_meals()
    return [meal for meal in all_meals if meal in needed_meals]

# comes from the filter_meals
def remove_dessert(filtered_meals):
    dessert_url = "https://www.themealdb.com/api/json/v1/1/filter.php?c=dessert"
    response = requests.get(dessert_url).json()

    if 'meals' in response:
        dessert_meals = [meal['strMeal'] for meal in response['meals']]
        filtered_meals = [meal for meal in filtered_meals if meal not in dessert_meals]
        filtered_meals = [meal for meal in filtered_meals if meal != "Vegan Chocolate Cake"]
        return filtered_meals
    

# need to do the remove dessert funtion before doing this functions
def breakfast_meals(filtered_meals):
    breakfast_url = "https://www.themealdb.com/api/json/v1/1/filter.php?c=breakfast"
    response = requests.get(breakfast_url).json()

    if 'meals' in response:
        breakfast_meals = [meal['strMeal'] for meal in response['meals']]
        filtered_meals = [meal for meal in filtered_meals if meal in breakfast_meals]

        if len(filtered_meals) >= 3:
            random_meals = random.sample(filtered_meals, 3)
        else:
            random_meals = filtered_meals
        return random_meals

# need to do the remove dessert funtion before doing this functions
def lunch_and_dinner_meals(filtered_meals):
     breakfast_url = "https://www.themealdb.com/api/json/v1/1/filter.php?c=breakfast"
     response = requests.get(breakfast_url).json()
     
     if 'meals' in response:
        breakfast_meals = [meal['strMeal'] for meal in response['meals']]
        filtered_meals = [meal for meal in filtered_meals if meal not in breakfast_meals]
        
        if len(filtered_meals) >= 6:
            random_meals = random.sample(filtered_meals, 6)
        else:
            random_meals = filtered_meals
        return random_meals
    
#comes from the filter_meals
def only_dessert(filtered_meals):
    dessert_url = "https://www.themealdb.com/api/json/v1/1/filter.php?c=dessert"
    response = requests.get(dessert_url).json()

    if 'meals' in response:
        dessert_meals = [meal['strMeal'] for meal in response['meals']]
        filtered_meals = [meal for meal in filtered_meals if meal in dessert_meals]

        if len(filtered_meals) >= 3:
            random_meals = random.sample(filtered_meals, 3)
        else:
            random_meals = filtered_meals
        return random_meals

def get_meal_ids(random_meals):
    """Fetch the meal IDs for given meal names."""
    meal_ids = []
    for meal_name in random_meals:
        try:
            search_url = f"https://www.themealdb.com/api/json/v1/1/search.php?s={meal_name}"
            response = requests.get(search_url).json()
            if response['meals']:
                meal_ids.append(response['meals'][0]['idMeal'])
        except Exception as e:
            print(f"Error fetching meal ID for {meal_name}: {e}")
    return meal_ids

def get_recipe(meal_id):
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

app = FastAPI()
class DietType(BaseModel):
    diet: str

@app.post("/diet-plan/")
def diet_plan(request: DietType):
    type_diet = request.diet_type

    # Get the list of ingredients based on the selected diet
    main_ingredients_avoid = healthy_lifestyle(type_diet)

    # Filter meals that contain the ingredients the user wants to avoid
    meals_avoid = filter_meals(main_ingredients_avoid)

    # Get all meals after filtering based on the avoidance list
    if type_diet == 'vegetarian':
        all_meals = vegeterian(meals_avoid)
    else:
        all_meals = carnivore_pescatarian(main_ingredients_avoid)

    # Remove dessert meals from the filtered list
    filter_no_dessert = remove_dessert(all_meals)

    # Fetch random breakfast, lunch & dinner, and dessert meals from the filtered list
    breakfast = breakfast_meals(filter_no_dessert)
    lunch_and_dinner = lunch_and_dinner_meals(filter_no_dessert)
    desserts = only_dessert(filter_no_dessert)

    # Get the meal IDs for the selected meals
    breakfast_ids = get_meal_ids(breakfast)
    lunch_and_dinner_ids = get_meal_ids(lunch_and_dinner)
    dessert_ids = get_meal_ids(desserts)

    # Fetch recipes for breakfast, lunch & dinner, and dessert meals
    breakfast_recipes = [get_recipe(meal_id) for meal_id in breakfast_ids]
    lunch_and_dinner_recipes = [get_recipe(meal_id) for meal_id in lunch_and_dinner_ids]
    dessert_recipes = [get_recipe(meal_id) for meal_id in dessert_ids]

    return {
        "breakfast_recipes": breakfast_recipes,
        "lunch_and_dinner_recipes": lunch_and_dinner_recipes,
        "dessert_recipes": dessert_recipes,
    }
