from pathlib import Path
from dataclasses import astuple

from Data.Mealplan.recipes import *
from Data.Exercise.exercise import *

from shopping_list_generator import send_current_shopping_list, re_roll_meal
from exercise_plan_generator import prev_weeks_last_gym_session

MEAL_PLAN_FILE = Path(r"Data\Mealplan\week_meal_plan.json")
WORKOUT_FILE = Path(r"Data\Exercise\week_workout_plan.json")

# re_roll_meal(MEAL_PLAN_FILE, "Harissa Pasta") #PASSES

# send_current_shopping_list(MEAL_PLAN_FILE) #PASSES

# print(prev_weeks_last_gym_session(WORKOUT_FILE)) #PASSES

# for item in Recipe.All_Recipes: #PASSES
#     print(astuple(item))

# for item in ALL_EXERCISES.exercises: #PASSES
#     print(Exercise.to_tuple(item))

# for i in Ingredient.All_Ingredients: #PASSES
#     values = astuple(i)
#     print(values)

# for r in Recipe.All_Recipes: #PASSES
#     print(astuple(r))

