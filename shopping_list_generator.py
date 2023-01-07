### Imports ###
import random
import json
from pathlib import Path

from Config.emails import send_email
from Config.config import SMTP_EMAIL, TO_FREYA

from Data.helpers import load_current_plan

import Data.Mealplan.recipes as r


#### TO-DO ####
"""
- Look into adding Alexa functionality to allow additions to the shopping list and/or meal plan.
- Re-rolling the whole plan.
- Re-rolling just one item.
- Look into receiving emails via the script.
"""

########### Meal Plan Functions ############

def generate_meal_plan(last_weeks_data: dict) -> list[r.Recipe]:
    """Generates a meal plan for the week, ensuring no meals from last week are included"""
    # Generate meals list without any of last weeks meals
    if last_weeks_data:
        eligble_meals = [meal for meal in r.Recipe.All_Recipes if meal.name not in last_weeks_data['Meal Plan']]
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


def save_new_meal_plan(MEAL_PLAN_FILE, meal_plan: list[str], ingredients_by_category: dict):
    """Takes the meal plan and unique ingredients to over-write last weeks meal plan"""
    with open(MEAL_PLAN_FILE, 'w') as f:
        data = {
            "Meal Plan": meal_plan,
            "Shopping List": ingredients_by_category
        }
        json.dump(data, f)

def send_current_shopping_list():
    """Sends a copy of the current shopping list to email."""
    current_meal_plan = load_current_plan(MEAL_PLAN_FILE)

    meal_plan_list = current_meal_plan['Meal Plan']
    ingredients_by_category = current_meal_plan['Shopping List']

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


### Constants ###
MEAL_PLAN_FILE = (r"Data\Mealplan\ingredients.json")

### Main ###
if __name__ == "__main__":
    """Main function is the generation of a new meal plan and resultant shopping list.
    This is emailed to both parties. 
    """
    # Get last plan for comparison
    try:
        last_weeks_data = load_current_plan(MEAL_PLAN_FILE)
    except:
        last_weeks_data = None

    # Generate the meal plan
    weekly_meal_plan = generate_meal_plan(last_weeks_data) #type: ignore

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
