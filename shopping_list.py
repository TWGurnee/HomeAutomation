import random
import recipes as r
from Config.emails import send_email

#### Food Ideas Section ####
"""
- Cous-Cous Honey and Garlic Prawns
- Roast shrimp and veggie salad
- More Salads & healthy options
"""
#### TO-DO ####
"""
- Categorise Foods for prettier list: Restucture ingredients (add weights/amounts, perhaps prices and calories)
- Compare to last weeks recipes to ensure variety?
- Re-rolling the whole thing?
- Re-rolling just one item?
- Look into receiving emails via the script?
"""
### Create helper objects for choosing function later.
# Create a list to hold the weekly meal plan
weekly_meal_plan = []

# Create a set to hold the ingredients for the shopping list
shopping_list = set()

meal_types = ['Tim', 'Freya', 'Healthy']

# randomly select 2 recipe objects of each type to add to the weekly meal plan
for type in meal_types:
  choices = random.sample([meal for meal in r.Recipe.All_Recipes if meal.type == type], 2)
  weekly_meal_plan.extend(choices)

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

# Create email message
msg = "This week's meal plan:\n" + meal_plan_string + '\nShopping list:\n' + shopping_list_string
subject = "Meal Plan"

# Send meal plan
send_email(subject, msg)