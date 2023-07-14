import sys
import time


from pathlib import Path
from dataclasses import astuple

from src.Data.Mealplan import *
from src.Data.Exercise import *
from src.Data.database_sqlite import Database, generate_exercise_session_by_type, get_workout_session

import src.Data.database_postgres as PSQL

from src.shopping_list_generator import *
from src.exercise_plan_generator import *
import src.workout_reminder

MEAL_PLAN_FILE = Path(r"src\Data\Mealplan\week_meal_plan.json")
WORKOUT_FILE = Path(r"src\Data\Exercise\week_workout_plan.json")

# re_roll_meal(MEAL_PLAN_FILE, "Prawn Chorizo Rice") #PASSES

# send_current_shopping_list(MEAL_PLAN_FILE) #PASSES

# print(prev_weeks_last_gym_session(WORKOUT_FILE, GYM_DAY_CONFIG)) #PASSES

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

# print(get_exercise_session_by_type(SessionType.BACK_CORE_ARMS)) #PASSES

# back_day = get_workout_session(day_type=SessionType.BACK_CORE_ARMS) #PASSES
# print(WorkoutSession.get_workout_session_key(back_day))

# print(current_weekly_workout_plan_for_dash(WORKOUT_FILE))

# print(simplified_weekly_workout_plan(WORKOUT_FILE))


# with Database() as db:
#     db.cursor.execute("""
#     INSERT INTO recipe_ingredients (ingredient_quantity, recipe_id, ingredient_id)
#     VALUES (?, ?, ?)""",
#     ())

# ingredients = Database.get_ingredients()

# for ingredient in ingredients:
#     PSQL.Database.add_ingredient(ingredient)

# recipes = Database.get_recipes()

# PSQL.Database.fill_recipes(recipes)


