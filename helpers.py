from shopping_list import get_all_ingredients_by_category
from Data.recipes import Recipe, Ingredient


Test = {('Tim', 'Steak'): ['Steak', 'Broccoli/Asparagus', 'Chips/Potatoes', 'Peppercorn Sauce']}

def generate_recipe(recipe_dict: dict) -> Recipe:
    meal_type, name = list(recipe_dict.keys())[0]
    ingredients = recipe_dict[(meal_type, name)]
    ingredient_objects = []
    for ingredient in ingredients:
        quantity = 1
        all_ingredient_categories = get_all_ingredients_by_category()
        all_categories, all_ingredients = all_ingredient_categories.items()
        if ingredient in all_ingredients:
            category = all_categories[ingredient]
        else:
            category = "UNCATEGORISED"
        ingredient_objects.append(Ingredient(name=ingredient, quantity=quantity, category=category))
    return Recipe(name=name, ingredients=ingredient_objects, type=meal_type)

print(generate_recipe(Test))