import random
import recipes as r
#from Config.emails import send_email

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

# update shopping list accordingly
# for meal in weekly_meal_plan:
#   shopping_list[]

"""
Each meal has list of ingredients
Each Ingredient is an object with a Category, name and quantity.
We want a list split by category, ensuring only one of each name is picked with the total quantity of the meal plan.
How can we arrange this?
"""

print(shopping_list)

# # print the weekly meal plan
# print(f"Weekly Meal Plan:\n{weekly_meal_plan}")

# # print the shopping list
# print(f"Shopping List:\n{shopping_list}")

# # Convert lists to strings:
# meal_plan_string = ', '.join(weekly_meal_plan)
# shopping_list_string = ', '.join(shopping_list)

# # Create email message
# msg = "This week's meal plan:\n" + meal_plan_string + '\nShopping list:\n' + shopping_list_string
# subject = "Meal Plan"

# # Send meal plan
# send_email(subject, msg)