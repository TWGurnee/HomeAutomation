import Data.recipes as r
from HomeAutomation.shopping_list import generate_ingredients_by_category

def get_all_ingredients_by_category():
    all_ingredients_by_category = generate_ingredients_by_category(r.Recipe.All_Recipes)
    return all_ingredients_by_category


#def generate_recipe(meal: dict):