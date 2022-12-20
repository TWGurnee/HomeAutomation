import random
from Config.emails import send_email

### Set meals cooked by each person
tims_meals = {
  "Burritos": ['Mince/Chicken', 'Onions', 'Peppers', 'Wraps', 'Cheddar', 'Avocado', 'Mushrooms', 'Leaves', 'Rice', 'Garlic'],
  "Indian Curry": ['Paste', 'Peppers', 'Onions', 'Mushrooms', 'Rice', 'Naan', 'Chutney', 'Yoghurt/Cream'],
  "Arrabiata": ['Chopped Tomatoes', 'Penne', 'Basil', 'Chili', 'Onions', 'Peppers', 'Mushrooms', 'Oregano'],
  "Thai Curry": ['Coconut Milk', 'Broccoli', 'Leaves', 'Green Beans', 'Peas', 'Chicken', 'Prawn Crackers', 'Onions'],
  "Burgers": ['Mince', 'Bread Rolls', 'Beef Tomato', 'Lettuce', 'Mustard', 'Parsley', 'Ketchup', 'Mayonnaise', 'Chips', 'Onions', 'American Mustard', 'Garlic'],
  "Pizza": ['Flatbread', 'Mozzarella', 'Parmesan', 'Pizza Toppings', 'Tomato Puree'],
  "Steak": ['Steak', 'Broccoli/Asparagus', 'Chips/Potatoes', 'Peppercorn Sauce'],
  "Quesadillas": ['Wraps', 'Chicken', 'Mushroom', 'Cheddar', 'Onions', 'Leaves'],
  "Creamy Pesto": ['Fusilli', 'Pesto', 'Cherry Tomatoes', 'Parmesan', 'Olive Oil', 'Double Cream', 'Basil', 'Oregano'],
  "Stir Fry": ['Stir Fry Sauce', 'Soy Sauce', 'Noodles', 'Mini-Corn', 'Beansprouts', 'Mushrooms', 'Chicken']
}

freyas_meals = {
  "Mac & Cheese": ['Macaroni', 'Butter', 'Milk', 'Cheddar'],
  "Sausage Pasta Bake": ['Red Wine', 'Rigatoni', 'Sausages', 'Carrots', 'Onions', 'Tomato Puree', 'Veg Stock', 'Milk', 'Flour', 'Cheese', 'Rosemary', 'Basil'],
  "Chicken Pie": ['Chicken', 'Pastry', 'Onions', 'Flour', 'Milk', 'Chicken Stock', 'White Wine', 'Potatoes', 'Thyme', 'Basil', 'Leeks'],
  "Salmon Tagiatelle": ['Salmon', 'Mushroom', 'Crème fraiche', 'Salt', 'Pepper', 'Lemon Juice'],
  "Chicken Stew": ['Chicken Thighs', 'Dijon Mustard', 'Crème fraiche', 'Veg Stock', 'Chicken Stock', 'Butter', 'Parsley', 'Peas', 'Leeks', 'Celery', 'Potatoes'],
  "Baked Potatoes": ['Baked Potatoes', 'Tuna', 'Mayonnaise', 'Baked Beans', 'Leaves', 'Butter'],
  "Salmon Fillet": ['Salmon', 'Potatoes', 'Broccoli/Asparagus', 'Butter', 'Oregano', 'Chili Flakes', 'Garlic'],
  "Harissa Pasta": ['Rigatoni', 'Rose Harissa Paste', 'Mascarpone', 'Sundried Tomato', 'Parmesan','Garlic', 'Fresh Basil'],
  "Chicken Alfredo": ['Penne', 'Low Fat Cream Cheese', 'Parmesan', 'Oat Milk', 'Flour', 'Garlic', 'Butter', 'Spinach'],
  "Katsu Curry": ['Chicken', 'Breadcrumbs', 'Rice', 'Onions', 'Garlic', 'Ginger', 'Turmeric', 'Mild Curry Powder', 'Flour', 'Veg Stock', 'Coconut Milk', 'Eggs', 'Leaves']
}

salads = {
  "Chicken Avocado Salad": ['Chicken', 'Leaves', 'Avocado', 'Onions', 'Peppers', 'Cucumber', 'Honey Mustard Dressing'],
  "Cod Mango Salad": ['Cod', 'Mango', 'Leaves', 'Avocado'],
  "Halloumi & Mango Salad": ['Halloumi', 'Mango', 'Rocket', 'Cherry Tomato'],
  "Greek Salad": ['Feta', 'Leaves', 'Olives', 'Cucumber', 'Sundried Tomato', 'Olive Oil', 'Balsamic Vinegar']
}

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

# Iterator to generate choices for weekly meal plan
meals = {
  "Tim": tims_meals,
  "Freya": freyas_meals,
  "Salads": salads
}

# Iterator for shopping list ingredients 
all_meals = tims_meals | freyas_meals | salads

# randomly select 2 meals from each list to add to the weekly meal plan
for name in meals.keys():
  choices = random.sample(list((meals[name]).keys()), 2) #list needed to avoid depreciation error
  weekly_meal_plan.extend(choices)

# update shopping list accordingly
for meal in weekly_meal_plan:
  shopping_list.update(all_meals[meal])

# print the weekly meal plan
print(f"Weekly Meal Plan:\n{weekly_meal_plan}")

# print the shopping list
print(f"Shopping List:\n{shopping_list}")

# Convert lists to strings:
meal_plan_string = ', '.join(weekly_meal_plan)
shopping_list_string = ', '.join(shopping_list)

# Create email message
msg = "This week's meal plan:\n" + meal_plan_string + '\nShopping list:\n' + shopping_list_string
subject = "Meal Plan"

# Send meal plan
send_email(subject, msg)