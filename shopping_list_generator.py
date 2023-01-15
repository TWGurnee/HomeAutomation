### Imports ###
import random
import json
from pathlib import Path

from Config.emails import send_email
from Config.config import SMTP_EMAIL, TO_FREYA

from Data.helpers import load_current_plan

import Data.Mealplan.recipes as r

### Constants ###
MEAL_PLAN_FILE = Path(r"Data\Mealplan\week_meal_plan.json") ##TODO perhaps move to config file?


### Helper methods

def unpack_saved_meal_plan(MEAL_PLAN_FILE):
    """Load the JSON file with saved meal plan and ingredients by category and unpack"""
    current_meal_plan = load_current_plan(MEAL_PLAN_FILE)
    meal_plan_list = current_meal_plan['Meal Plan']
    ingredients_by_category = current_meal_plan['Shopping List']
    return (meal_plan_list, ingredients_by_category)


def save_new_meal_plan(MEAL_PLAN_FILE, meal_plan: list[str], ingredients_by_category: dict):
    """Takes the meal plan and unique ingredients to over-write last weeks meal plan"""
    with open(MEAL_PLAN_FILE, 'w') as f:
        data = {
            "Meal Plan": meal_plan,
            "Shopping List": ingredients_by_category
        }
        json.dump(data, f)


########### Meal Plan Functions ############

def generate_meal_plan(last_weeks_meals=None) -> list[r.Recipe]:
    """Generates a meal plan for the week, ensuring no meals from last week are included"""
    # Generate meals list without any of last weeks meals
    if last_weeks_meals:
        eligble_meals = [meal for meal in r.Recipe.All_Recipes if meal.name not in last_weeks_meals]
    else:
        eligble_meals = r.Recipe.All_Recipes

    # Create a list to hold the weekly meal plan
    weekly_meal_plan = []

    # Meal types to ensure healthy plan and fair cooking responsibilities
    meal_types = ['Tim', 'Freya', 'Healthy']
    #meal_types = {meal.type for meal in r.Recipe.All_Recipes}

    # randomly select 2 eligible recipe objects of each type to add to the weekly meal plan
    for type in meal_types:
        choices = random.sample([meal for meal in eligble_meals if meal.type == type], 2)
        weekly_meal_plan.extend(choices)

    return weekly_meal_plan


def update_ingredients_by_category(ingredient: r.Ingredient, ingredients_by_category: dict):
    """Update the ingredients_by_category dict with a new ingredient."""
    # If the category doesn't exist in the dictionary yet, add it
    if ingredient.category not in ingredients_by_category:
        ingredients_by_category[ingredient.category] = {}
    
    # If the ingredient name doesn't exist in the dictionary yet, add it
    if ingredient.name not in ingredients_by_category[ingredient.category]:
        ingredients_by_category[ingredient.category][ingredient.name] = ingredient.quantity
    
    # If the ingredient name does exist, add the quantity to the existing value
    else:
        ingredients_by_category[ingredient.category][ingredient.name] += ingredient.quantity


def generate_ingredients_by_category(weekly_meal_plan: list[r.Recipe]) -> dict:
    """Returns a dict of all the unique ingredients and their quantities in the weekly meal plan"""
    # Create a dictionary to hold the ingredients by category
    ingredients_by_category = {}

    # Iterate through the weekly meal plan and add the ingredients to the dictionary
    for meal in weekly_meal_plan:
        for ingredient in meal.ingredients:
            update_ingredients_by_category(ingredient, ingredients_by_category)

    return ingredients_by_category


def generate_shopping_list(ingredients_by_category: dict) -> str:
    """Returns a nicely formatted shopping_list from a nested dict of unique ingredients"""
    # Create an empty string to hold the output
    shopping_list_string = ""

    # Iterate through the dictionary and build the output string
    for category, ingredients in ingredients_by_category.items():
        # Add the category name to the output string
        shopping_list_string += f"\n{category}:\n"
        # Iterate through the ingredients and add their names and quantities to the output string
        for name, quantity in ingredients.items():
            shopping_list_string += f"- {name}: {quantity}\n"

    return shopping_list_string


def send_current_shopping_list(MEAL_PLAN_FILE):
    """Sends a copy of the current shopping list to email."""

    meal_plan_list, ingredients_by_category = unpack_saved_meal_plan(MEAL_PLAN_FILE)

    # Convert plan and ingredients to strings for email
    shopping_list_string = generate_shopping_list(ingredients_by_category)
    meal_plan_string = ', '.join(meal_plan_list)

    # Create email message
    msg = "This week's meal plan:\n" + meal_plan_string + \
           '\nShopping list:\n' + shopping_list_string
    subject = "Meal Plan"

    # Log to CLI
    print("This week's meal plan:\n" + meal_plan_string)

    # Send meal plan to emails
    send_email(subject, msg, SMTP_EMAIL)
    send_email(subject, msg, TO_FREYA)


####### Dashboard functions ###########

def current_meal_plan_for_table(MEAL_PLAN_FILE) -> list[tuple[str, str, str]]: #MESSY but accurate
    """Returns a list of packed meal-strings to be shown in a table.
    Table headers are:
    Category, Meal, Ingredients
    Returns (meal type, meal name, [ingredients])"""

    meal_plan_list, ingredients_by_category = unpack_saved_meal_plan(MEAL_PLAN_FILE)

    def pack_meal_info(meal_name):
        recipe = r.Recipe.get_recipe_from_name(meal_name)
        return (recipe.type, meal_name, ', '.join([i.name for i in recipe.ingredients])) #type: ignore

    # week_meal_plan_info = current_meal_plan_for_table()
    # {% for meal in week_plan_meal_info %}
    """
    <tr>
        <td>
            {{meal[0]}}
        </td>
        <td>
            {{meal[1]}}
        </td>
        <td>
            {{meal[2]}}
        </td>
    </tr>
    """
    # {% endfor %}

    return [pack_meal_info(meal) for meal in meal_plan_list]


def re_roll_meal(MEAL_PLAN_FILE, meal_name: str): ## DEPRECIATED, will not be used in dashboard
    """Rerolls a single named meal in the meal plan"""
    meal_plan_list, ingredients_by_category = unpack_saved_meal_plan(MEAL_PLAN_FILE)

    old_meal = r.Recipe.get_recipe_from_name(meal_name)

    new_meal = random.choice([meal for meal in r.Recipe.All_Recipes if meal.type == old_meal.type if meal.name not in meal_plan_list]) #type: ignore

    meal_plan_list[meal_plan_list.index(meal_name)] = new_meal.name

    recipe_list = [r.Recipe.get_recipe_from_name(meal) for meal in meal_plan_list]

    ingredients_by_category = generate_ingredients_by_category(recipe_list) #type: ignore

    print(meal_plan_list)

    save_new_meal_plan(MEAL_PLAN_FILE, meal_plan_list, ingredients_by_category)

    return current_meal_plan_for_table(MEAL_PLAN_FILE)


def re_roll_selection(MEAL_PLAN_FILE, meal_name_list: list["str"]):
    """Rerolls a list of meals chosen in the dashboard mealplan table"""
    meal_plan_list, ingredients_by_category = unpack_saved_meal_plan(MEAL_PLAN_FILE)

    replaced_meals = [r.Recipe.get_recipe_from_name(meal_name) for meal_name in meal_name_list]

    for meal in replaced_meals:
        new_meal = (random.choice([recipe for recipe in r.Recipe.All_Recipes if recipe.type == meal.type if recipe.name not in meal_plan_list])) #type: ignore
        meal_plan_list[meal_plan_list.index(meal.name)] = new_meal.name #type: ignore

    recipe_list = [r.Recipe.get_recipe_from_name(meal) for meal in meal_plan_list]

    ingredients_by_category = generate_ingredients_by_category(recipe_list) #type: ignore

    save_new_meal_plan(MEAL_PLAN_FILE, meal_plan_list, ingredients_by_category)

    return current_meal_plan_for_table(MEAL_PLAN_FILE)


### Replace meal with specific choice
# TODO dropdown menu showing all mealsto specifically replace a meal with? Perhaps a popup with a dropdown list?



### Main ###
if __name__ == "__main__":
    """Main function is the generation of a new meal plan and resultant shopping list.
    This is emailed to both parties. 
    """
    # Get last plan for comparison
    meal_plan_list, ingredients_by_category = unpack_saved_meal_plan(MEAL_PLAN_FILE)

    # Generate the meal plan
    weekly_meal_plan = generate_meal_plan(meal_plan_list) #type: ignore

    # Create meal plan dict for shopping list generation
    ingredients_by_category = generate_ingredients_by_category(weekly_meal_plan)

    # Convert meal plan to strings for emailing and saving:
    meal_plan_list = [meal.name for meal in weekly_meal_plan]

    save_new_meal_plan(MEAL_PLAN_FILE, meal_plan_list, ingredients_by_category)

    # Convert plan and ingredients to strings for email
    shopping_list_string = generate_shopping_list(ingredients_by_category)
    meal_plan_string = ', '.join(meal_plan_list)

    # Create email message
    msg = "This week's meal plan:\n" + meal_plan_string + \
           '\nShopping list:\n' + shopping_list_string
    subject = "Meal Plan"

    # Log to CLI
    print("This week's meal plan:\n" + meal_plan_string)

    # Send meal plan to emails
    send_email(subject, msg, SMTP_EMAIL)
    send_email(subject, msg, TO_FREYA)
