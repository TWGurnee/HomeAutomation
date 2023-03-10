### Imports ###
import random
import json
from pathlib import Path

from .Config.emails import send_email
from .Config.config import SMTP_EMAIL, TO_FREYA

from .Data.helpers import load_current_plan
from .Data.database_sqlite import Database

from .Data.Mealplan import Ingredient, Recipe

### Constants ###
MEAL_PLAN_FILE = Path(r"src\Data\Mealplan\week_meal_plan.json") ##TODO perhaps move to config file?


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

def generate_meal_plan(last_weeks_meals=None) -> list[Recipe]:
    """Generates a meal plan for the week, ensuring no meals from last week are included"""
    # Generate meals list without any of last weeks meals
    if last_weeks_meals:
        eligble_meals = [meal for meal in Database.get_recipes() if meal.name not in last_weeks_meals] # type: ignore
    else:
        eligble_meals = Database.get_recipes()

    # Create a list to hold the weekly meal plan
    weekly_meal_plan = []

    # Meal types to ensure healthy plan and fair cooking responsibilities
    meal_types = ['Tim', 'Freya', 'Healthy']
    #meal_types = {meal.type for meal in Database.get_recipes()}

    # randomly select 2 eligible recipe objects of each type to add to the weekly meal plan
    for type in meal_types:
        choices = random.sample([meal for meal in eligble_meals if meal.type == type], 2) #type: ignore
        weekly_meal_plan.extend(choices)

    return weekly_meal_plan


def update_ingredients_by_category(ingredient: Ingredient, ingredients_by_category: dict) -> None:
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


def generate_ingredients_by_category(weekly_meal_plan: list[Recipe]) -> dict[str, str]:
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
        recipe = Database.get_recipe_from_name(meal_name)
        return (recipe.type, meal_name, ', '.join([i.name for i in recipe.ingredients])) #type: ignore

    return [pack_meal_info(meal) for meal in meal_plan_list]


def shopping_list_for_table(MEAL_PLAN_FILE):

    meal_plan_list, ingredients_by_category = unpack_saved_meal_plan(MEAL_PLAN_FILE)

    categories = list(ingredients_by_category.keys())
    ingredients_per_category = list(ingredients_by_category.values())
    ingredients = [list(i.keys()) for i in ingredients_per_category]

    return [(category, ingredient) for category, ingredient in zip(categories, ingredients)]


def shopping_list_for_textbox(MEAL_PLAN_FILE):
    meal_plan_list, ingredients_by_category = unpack_saved_meal_plan(MEAL_PLAN_FILE)
    shopping_list_string = generate_shopping_list(ingredients_by_category)
    return shopping_list_string


def re_roll_meal(MEAL_PLAN_FILE, meal: str | int):
    """Rerolls a single named meal in the meal plan"""
    meal_plan_list, ingredients_by_category = unpack_saved_meal_plan(MEAL_PLAN_FILE)

    def replace_meal(meal: str, meal_plan_list: list[str]):
        old_meal = Database.get_recipe_from_name(meal)

        new_meal = random.choice([meal for meal in Database.get_recipes() if meal.type == old_meal.type if meal.name not in meal_plan_list]) #type: ignore

        try:
            meal_plan_list[meal_plan_list.index(meal)] = new_meal.name 
        except ValueError as e:
            print(f'{e}: Re-roll another meal')


    if isinstance(meal, str):
        replace_meal(meal, meal_plan_list)

    elif isinstance(meal, int):
        old_meal = meal_plan_list[meal]
        replace_meal(old_meal, meal_plan_list)

    recipe_list = [Database.get_recipe_from_name(meal) for meal in meal_plan_list]

    ingredients_by_category = generate_ingredients_by_category(recipe_list) 

    # print(meal_plan_list)

    save_new_meal_plan(MEAL_PLAN_FILE, meal_plan_list, ingredients_by_category)

    return current_meal_plan_for_table(MEAL_PLAN_FILE)


def re_roll_selection(MEAL_PLAN_FILE, meal_name_list: list[str]):
    """Rerolls a list of meals chosen in the dashboard mealplan table"""
    meal_plan_list, ingredients_by_category = unpack_saved_meal_plan(MEAL_PLAN_FILE)

    replaced_meals = [Database.get_recipe_from_name(meal_name) for meal_name in meal_name_list]

    for meal in replaced_meals:
        new_meal = (random.choice([recipe for recipe in Database.get_recipes() if recipe.type == meal.type if recipe.name not in meal_plan_list])) #type: ignore
        try:
            meal_plan_list[meal_plan_list.index(meal)] = new_meal.name
        except ValueError as e:
            print(f'{e}: Re-roll another meal')

    recipe_list = [Database.get_recipe_from_name(meal) for meal in meal_plan_list]

    ingredients_by_category = generate_ingredients_by_category(recipe_list) #type: ignore

    save_new_meal_plan(MEAL_PLAN_FILE, meal_plan_list, ingredients_by_category)

    return current_meal_plan_for_table(MEAL_PLAN_FILE)


def remove_selected_items_from_shoppinglist(MEAL_PLAN_FILE, category: str, items: list[str]):

    meal_plan_list, ingredients_by_category = unpack_saved_meal_plan(MEAL_PLAN_FILE)

    #remove items from teh category
    category_with_items = ingredients_by_category.get(category)
    for item in items:
        del category_with_items[item]

    ingredients_by_category[category] = category_with_items

    save_new_meal_plan(MEAL_PLAN_FILE, meal_plan_list, ingredients_by_category)


### Replace meal with specific choice
# TODO dropdown menu showing all mealsto specifically replace a meal with? Perhaps a popup with a dropdown list?

### Main ###

def main():
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
    print(f'Mealplans sent to: {SMTP_EMAIL, TO_FREYA}')


if __name__ == "__main__":
    main()
