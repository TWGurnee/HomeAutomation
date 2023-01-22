from dataclasses import dataclass
from ..database_sqlite import *


@dataclass(frozen=True)
class Ingredient:
    name: str
    quantity: int
    category: str

    # All_Ingredients = []

    # def __post_init__(self):
    #     if self not in self.__class__.All_Ingredients:
    #         self.__class__.All_Ingredients.append(self)


# def categorise_ingredient(ingredient: Ingredient) -> str:
#     """Get or assign category for a ingredient.name or string"""
    
#     # To get categories we need all current ingredients and their category.
#     all_ingredient_names = [ingredient.name for ingredient in Ingredient.All_Ingredients]
#     get_category_from_name = {i.name: i.category for i in Ingredient.All_Ingredients}
    
#     # Categorise ingredient
#     if ingredient in all_ingredient_names:
#         category = get_category_from_name[ingredient]
#     else:
#         category = "UNCATEGORISED"
    
#     return category


@dataclass(frozen=True)
class Recipe:
    name: str
    ingredients: list[Ingredient]
    type: str

    # All_Recipes = []

    # def __post_init__(self):
    #     self.__class__.All_Recipes.append(self)

    # @staticmethod
    # def generate_recipe(recipe_dict: dict):
    #     """Helper method to generate recipes from a simple typed input dict:
    #     For example: 
    #     `Test_Recipe = {('Tim', 'Steak'): ['Steak', 'Broccoli/Asparagus', 'Chips/Potatoes', 'Peppercorn Sauce']}`
    #     `generate_recipe(Test_Recipe)`
    #     Would give the steak recipe reflected below. 
    #     Currently result is unformatted and works on dicts of 1 recipe"""

    #     # Unpack input:
    #     meal_type, name = list(recipe_dict.keys())[0]
    #     ingredients = recipe_dict[(meal_type, name)]

    #     # Create list to hold the ingredients for building Recipe object.
    #     ingredient_objects = []

    #     # Fill ingredient_objects list
    #     for ingredient in ingredients:
    #         # Generic quantity value
    #         quantity = 1

    #         # Get category
    #         category = categorise_ingredient(ingredient)

    #         # Add to list
    #         ingredient_objects.append(Ingredient(
    #             name=ingredient, quantity=quantity, category=category))

    #     return Recipe(name=name, ingredients=ingredient_objects, type=meal_type)

    # @staticmethod
    # def get_recipe_from_name(name: str):
    #     get_meal = {meal.name: meal for meal in Recipe.All_Recipes}
    #     return get_meal.get(name)


#### Food Ideas ####
"""
- Roast shrimp and veggie salad
- More Salads & healthy options
"""

# Ingredient.categories:
# Meat (includes fish)
# Veg
# Frozen
# Beverages
# Long-life
# Dairy
# Condiment
# Bread
# Herbs/Spices