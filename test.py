import sys

from pathlib import Path
from dataclasses import astuple

from Data.Mealplan import *
from Data.Exercise import *
from Data.database_sqlite import Database, get_exercise_session_by_type

from shopping_list_generator import *
from exercise_plan_generator import *

MEAL_PLAN_FILE = Path(r"Data\Mealplan\week_meal_plan.json")
WORKOUT_FILE = Path(r"Data\Exercise\week_workout_plan.json")

# re_roll_meal(MEAL_PLAN_FILE, "Prawn Chorizo Rice") #PASSES

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

# print(get_recipe_from_name('Burritos')) #PASSES

# for e in Database.get_exercises(SessionType.CHEST_SHOULDERS): #PASSES
#     print(e.name)

# print(get_exercise_session_by_type(SessionType.BACK_CORE_ARMS))