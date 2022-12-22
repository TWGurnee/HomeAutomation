### Imports ###
import random
import json

import Data.recipes as r
from Config.emails import send_email
from Config.config import SMTP_EMAIL, TO_FREYA


#### TO-DO ####
"""
- Look into adding Alexa functionality to allow additions to the shopping list and/or meal plan.
- Re-rolling the whole plan.
- Re-rolling just one item.
- Look into receiving emails via the script.
"""

########### Meal Plan Functions ############


def get_last_weeks_data(MEAL_PLAN_FILE):
    """Returns dict of last weeks meal plan and ingredients"""
    with open(MEAL_PLAN_FILE, 'r') as f:
        try:
            last_weeks_data = json.load(f)
        except Exception as e:
            last_weeks_data = None
            print(e)
        return last_weeks_data


def generate_meal_plan(last_weeks_data) -> list[r.Recipe]:
    """Generates a meal plan for the week, ensuring no meals from last week are included"""
    # Generate meals list without any of last weeks meals
    if last_weeks_data:
        eligble_meals = [
            meal for meal in r.Recipe.All_Recipes if meal.name not in last_weeks_data['Meal Plan']]
    else:
        eligble_meals = r.Recipe.All_Recipes

    # Create a list to hold the weekly meal plan
    weekly_meal_plan = []

    # Meal types to ensure healthy plan and fair cooking responsibilities
    meal_types = ['Tim', 'Freya', 'Healthy']

    # randomly select 2 eligible recipe objects of each type to add to the weekly meal plan
    for type in meal_types:
        choices = random.sample(
            [meal for meal in eligble_meals if meal.type == type], 2)
        weekly_meal_plan.extend(choices)

    return weekly_meal_plan


def generate_ingredients_by_category(weekly_meal_plan: list[r.Recipe]) -> dict:
    """Returns a dict of all the unique ingredients and their quantities in the weekly meal plan"""
    # Create a dictionary to hold the ingredients by category
    ingredients_by_category = {}

    # Iterate through the weekly meal plan and add the ingredients to the dictionary
    for meal in weekly_meal_plan:
        for ingredient in meal.ingredients:
            # If the category doesn't exist in the dictionary yet, add it
            if ingredient.category not in ingredients_by_category:
                ingredients_by_category[ingredient.category] = {}

            # If the ingredient name doesn't exist in the dictionary yet, add it
            if ingredient.name not in ingredients_by_category[ingredient.category]:
                ingredients_by_category[ingredient.category][ingredient.name] = ingredient.quantity

            # If the ingredient name does exist, add the quantity to the existing value
            else:
                ingredients_by_category[ingredient.category][ingredient.name] += ingredient.quantity

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


def save_current_meal_plan(MEAL_PLAN_FILE, meal_plan_list: list[str], ingredients_by_category: dict):
    """Takes the meal plan and unique ingredients to over-write last weeks meal plan"""
    with open(MEAL_PLAN_FILE, 'w') as f:
        data = {
            "Meal Plan": meal_plan_list,
            "Shopping List": ingredients_by_category
        }
        json.dump(data, f)


### Constants ###
MEAL_PLAN_FILE = r"HomeAutomation\Data\ingredients.json"

### Main ###
if __name__ == "__main__":
    # Get last plan for comparison
    last_weeks_data = get_last_weeks_data(MEAL_PLAN_FILE)

    # Generate the meal plan
    weekly_meal_plan = generate_meal_plan(last_weeks_data)

    # Create meal plan dict for shopping list generation
    ingredients_by_category = generate_ingredients_by_category(
        weekly_meal_plan)

    # Convert meal plan to strings for emailing and saving:
    meal_plan_list = [meal.name for meal in weekly_meal_plan]

    save_current_meal_plan(MEAL_PLAN_FILE, meal_plan_list,
                           ingredients_by_category)

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
