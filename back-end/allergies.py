import requests
import random
from fastapi import FastAPI
from pydantic import BaseModel

#add more ingrediants to avoid
def main_allergy(allergies):
    main_ingredients = []
    if allergies == 'lactose':
        main_ingredients = ['Milk', 'Butter', 'Creme Fraiche', 'Greak Yogurt', 'Coconut Milk', 'Mascarpone', 'Full fat yogurt', 
                            'Mozzarella', 'Mozzarella Balls', 'Parmesan Cheese', 'Cheese', 'Cheese Curds', 'Sour Cream', 
                            'cream cheese', 'Condensed Milk', 'Heavy Cream', 'Whole Milk', 'Double Cream', 'Parmesan', 'Cubed Feta Cheese',
                            'Feta', 'Shredded Mexican Cheese', 'Pecorino', 'Cheddar Cheese']
    elif allergies == 'celiac disease':
        main_ingredients = ['flour', 'couscous', 'bread', 'Lasagne Sheets', 'rice', 'rice noodles', 'farfalle', 'rice stick noodles', 
                            'plain flour', 'Self-raising Flour', 'Fettuccine', 'Breadcrumbs', 'Suet', 'Spaghetti', 'Bun', 'Pita Bread', 
                            'Quinoa', 'Hard Taco Shells', 'Rigatoni', 'Puff Pastry', 'Macaroni', 'Corn Tortillas', 'Noodles']
    elif allergies == 'nut allergy':
        main_ingredients = ['peanuts','almonds', 'chestnuts', 'Peanut Butter', 'Pecan Nuts', 'Cashew Nuts', 'Fennel Seeds']
    elif allergies == 'crustacean shellfish':
        main_ingredients = ['clams', 'oysters', 'mussels', 'prawns', 'Raw King Prawns']
    else:
       raise ValueError

    return main_ingredients

def avoid_meals(main_ingredients_avoid):
    filter_url = "https://www.themealdb.com/api/json/v1/1/filter.php?i="
    avoiding_meals = set()  
    
    for ingredient in main_ingredients_avoid:
        main_url = filter_url + ingredient
        response = requests.get(main_url).json()
        
        if 'meals' in response and response['meals']:  
            meal_names = [meal['strMeal'] for meal in response['meals']]
            avoiding_meals.update(meal_names) 
    
    return list(avoiding_meals)

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

def filter_meals(all_meals, meals_to_avoid):
    return [meal for meal in all_meals if meal not in meals_to_avoid]


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

class AllergyType(BaseModel):
    allergy: str

@app.post("/filter-meals/")
def filter_meals_endpoint(request: AllergyType):
    allergy = request.allergy
    main_ingredients_avoid = main_allergy(allergy)
    meals_avoid = avoid_meals(main_ingredients_avoid)
    all_meals = get_all_meals()
    filter_meal = filter_meals(all_meals, meals_avoid)
    filter_no_dessert = remove_dessert(filter_meal)

    breakfast = breakfast_meals(filter_no_dessert)
    breakfast_ids = get_meal_ids(breakfast)

    lunch_and_dinner = lunch_and_dinner_meals(filter_no_dessert)
    lunch_and_dinner_ids = get_meal_ids(lunch_and_dinner)

    desserts = only_dessert(filter_meal)
    dessert_ids = get_meal_ids(desserts)

    breakfast_recipes = [get_recipe(meal_id) for meal_id in breakfast_ids]
    lunch_and_dinner_recipes = [get_recipe(meal_id) for meal_id in lunch_and_dinner_ids]
    dessert_recipes = [get_recipe(meal_id) for meal_id in dessert_ids]

    return {
        "breakfast_recipes": breakfast_recipes,
        "lunch_and_dinner_recipes": lunch_and_dinner_recipes,
        "dessert_recipes": dessert_recipes,
    }

