from typing import Dict #, List
from dataclasses import dataclass
from enum import Enum

@dataclass
class Ingredient:
    name: str
    recipe: str
    quantity: int
    choices: str=None
    category: str=None

@dataclass
class Recipe:
    name: str
    ingredients: list
    type: str

class FoodCategory(Enum):
    FRUIT = 1
    VEGETABLE = 2
    MEAT = 3
    POULTRY = 4
    SEAFOOD = 5
    DAIRY = 6
    BAKED_GOODS = 7
    CONDIMENTS = 8
    SNACKS = 9
    BEVERAGES = 10
    FROZEN = 11

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

all_meals = tims_meals | freyas_meals | salads



def create_recipes(tims_meals: dict) -> list[Recipe]:
    recipes = []
    for recipe_name, ingredients in tims_meals.items():
        recipe = Recipe(recipe_name, [], "Tim")
        for ingredient in ingredients:
            ingredient_obj = Ingredient(ingredient, recipe_name, 1)
            recipe.ingredients.append(ingredient_obj)
        recipes.append(recipe)
    return recipes

tims_recipes = create_recipes(tims_meals)

for recipe in tims_recipes:
    print(f"{recipe}\n")

# Recipes list:
# Burritos
# Indian Curry
# Arrabiata
# Thai Curry
# Burgers
# Pizza
# Steak
# Quesadillas
# Creamy Pesto
# Stir Fry
# Mac & Cheese
# Sausage Pasta Bake   
# Chicken Pie
# Salmon Tagiatelle    
# Chicken Stew
# Baked Potatoes       
# Salmon Fillet        
# Harissa Pasta        
# Chicken Alfredo      
# Katsu Curry
# Chicken Avocado Salad
# Cod Mango Salad
# Halloumi & Mango Salad
# Greek Salad

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# Ingredients list: 
# Salmon Fillet
# Curry Paste
# Breadcrumbs
# Mascarpone
# Ketchup
# Rigatoni
# Olives
# Honey Mustard Dressing
# Halloumi
# Baked Potatoes        
# Chili
# Tuna
# Ginger
# Pesto
# Chopped Tomatoes      
# Mini-Corn
# Sundried Tomato       
# Tomato Puree
# White Wine
# Veg Stock
# Dijon Mustard
# Fresh Basil
# Cheddar
# Prawn Crackers
# Flour
# Rice
# Macaroni
# Mango
# Pastry
# Broccoli
# Soy Sauce
# Mince/Chicken ####TODO
# Lettuce
# Butter
# Mushroom
# Leaves
# Mustard
# Noodles
# Pepper
# Feta
# Spinach
# Mayonnaise
# Penne
# Celery
# Beansprouts
# Low Fat Cream Cheese
# Bread Rolls
# Peppers
# Eggs
# Coconut Milk
# Peas
# Chili Flakes
# Garlic
# Sausages
# Cherry Tomatoes
# Turmeric
# Mushrooms
# Pizza Toppings
# Lemon Juice
# Salt
# Chicken Stock
# Steak
# Yoghurt/Cream
# Beef Tomato
# Milk
# Cucumber
# Carrots
# Peppercorn Sauce
# Rose Harissa Paste
# Cod
# Potatoes
# Olive Oil
# Balsamic Vinegar
# Parmesan
# Flatbread
# Baked Beans
# Wraps
# Mozzarella
# Rosemary
# Chips
# Oregano
# Cherry Tomato
# Leeks
# Naan
# American Mustard
# Rocket
# Fusilli
# Chutney
# Double Cream
# Stir Fry Sauce
# Chicken Thighs
# Green Beans
# Parsley
# Chicken
# Chips/Potatoes ###TODO
# Red Wine
# Oat Milk
# Avocado
# Crème fraiche
# Broccoli/Asparagus ###TODO
# Cheese
# Onions
# Basil
# Mild Curry Powder
# Mince
# Thyme