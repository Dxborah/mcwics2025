import requests
import random
from fastapi import FastAPI
from pydantic import BaseModel

def healthy_lifestyle_else(type_diet):
    main_ingredients = []
    if type_diet == 'carnivore diet':
        main_ingredients = ['Chicken Breasts', 'Lamb', 'Beef Fillet', 'Parma Ham', 'Beef', 'Beef Stock', 'Bacon', 'Chicken', 'Pork', 'Chicken Stock' ]
    elif type_diet == 'pescatarian':
        main_ingredients = ['Salmon', 'Prawns', 'clams', 'oysters', 'mussels', 'Raw King Prawns', 'Monkfish']

    return main_ingredients

def vegetarian_categorie():
    all_meals = []
    category_url = 'https://www.themealdb.com/api/json/v1/1/filter.php?c=Vegetarian'
    response = requests.get(category_url).json()
    if response and response['meals']:
        meals = [meal['strMeal'] for meal in response['meals']]
        all_meals.extend(meals)
    return all_meals

def needed_meals(main_ingredients):
    filter_url = "https://www.themealdb.com/api/json/v1/1/filter.php?i="
    needed_meal = set()
    
    for ingredient in main_ingredients:
        main_url = filter_url + ingredient
        response = requests.get(main_url).json()
        
        if 'meals' in response and response['meals']:  
            meal_names = [meal['strMeal'] for meal in response['meals']]
            needed_meal.update(meal_names) 
    
    return list(needed_meal)

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

def get_meal_ids(meal_names):
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

def get_recipe(meals_id):
    for meal_id in meals_id:
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
    type_diet = 'request.diet'  # Now it uses the provided diet from the request
    if type_diet == 'vegetarian':
        filtered_meal = vegetarian_categorie()
    else:
        main_ingrediants = healthy_lifestyle_else(type_diet)
        filtered_meal = needed_meals(main_ingrediants)
    
    dessert_removed = remove_dessert(filtered_meal)
    breakfast= breakfast_meals(dessert_removed)
    lunch_and_dinner = lunch_and_dinner_meals(dessert_removed)
    desserts = only_dessert(filtered_meal)

    dessert_ids = get_meal_ids(desserts)
    lunch_and_dinner_ids = get_meal_ids(lunch_and_dinner)
    breakfast_ids = get_meal_ids(breakfast)

    breakfast_recipes = get_recipe(breakfast_ids)
    lunch_and_dinner_recipes = get_recipe(lunch_and_dinner_ids)
    dessert_recipes = get_recipe(dessert_ids)

    return {
        "breakfast_recipes": breakfast_recipes,
        "lunch_and_dinner_recipes": lunch_and_dinner_recipes,
        "dessert_recipes": dessert_recipes,
    }

