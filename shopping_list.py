import random
import Data.recipes as r
from Config.emails import send_email
from Config.config import SMTP_EMAIL, TO_FREYA
import json

#### TO-DO ####
"""
- Look into adding Alexa functionality to allow additions to the shopping list and/or meal plan.
- Re-rolling the whole plan.
- Re-rolling just one item.
- Look into receiving emails via the script.
"""

# Check last weeks info and assign to variable

LAST_WEEKS_LIST = r"Data\ingredients.json"

with open(LAST_WEEKS_LIST, 'r') as f:
    try:
        last_weeks_data = json.load(f)
    except Exception as e:
        last_weeks_data = None
        print(e)

# Generate meals list without any of last weeks meals
if last_weeks_data:
    eligble_meals = [meal for meal in r.Recipe.All_Recipes if meal.name not in last_weeks_data['Meal Plan']]
else:
    eligble_meals = r.Recipe.All_Recipes

# Create a list to hold the weekly meal plan
weekly_meal_plan = []

# Meal types to ensure healthy plan and fair cooking responsibilities
meal_types = ['Tim', 'Freya', 'Healthy']

# randomly select 2 eligible recipe objects of each type to add to the weekly meal plan
for type in meal_types:
  choices = random.sample([meal for meal in eligble_meals if meal.type == type], 2)
  weekly_meal_plan.extend(choices)

# Create a dictionary to hold the ingredients by category
ingredients_by_category = {}

# Iterate through the weekly meal plan and add the ingredients to the dictionary
for meal in weekly_meal_plan:
    for ingredient in meal.ingredients:
        # If the category doesn't exist in the dictionary yet, add it
        if ingredient.category not in ingredients_by_category:
            ingredients_by_category[ingredient.category] = {}

        ## TODO add if ingredient.choices: to add details for multiple choice options

        # If the ingredient name doesn't exist in the dictionary yet, add it
        if ingredient.name not in ingredients_by_category[ingredient.category]:
            ingredients_by_category[ingredient.category][ingredient.name] = ingredient.quantity

        # If the ingredient name does exist, add the quantity to the existing value
        else:
            ingredients_by_category[ingredient.category][ingredient.name] += ingredient.quantity

# Create an empty string to hold the output
shopping_list_string = ""

# Iterate through the dictionary and build the output string
for category, ingredients in ingredients_by_category.items():
    # Add the category name to the output string
    shopping_list_string += f"\n{category}:\n"
    # Iterate through the ingredients and add their names and quantities to the output string
    for name, quantity in ingredients.items():
        shopping_list_string += f"- {name}: {quantity}\n"

# Convert lists to strings:
meal_plan_list = [meal.name for meal in weekly_meal_plan]
meal_plan_string = ', '.join(meal_plan_list)

# Over-write last weeks meal plan
with open(LAST_WEEKS_LIST, 'w') as f:
    data = {
        "Meal Plan": meal_plan_list,
        "Shopping List" : ingredients_by_category
        }
    json.dump(data, f)

print("This week's meal plan:\n" + meal_plan_string)

# Create email message
msg = "This week's meal plan:\n" + meal_plan_string + '\nShopping list:\n' + shopping_list_string
subject = "Meal Plan"

# Send meal plan
send_email(subject, msg, SMTP_EMAIL)
send_email(subject, msg, TO_FREYA)