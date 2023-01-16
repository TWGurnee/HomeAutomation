from pathlib import Path

from shopping_list_generator import send_current_shopping_list, re_roll_meal
import Data.Mealplan.recipes as r
from exercise_plan_generator import prev_weeks_last_gym_session

MEAL_PLAN_FILE = Path(r"Data\Mealplan\week_meal_plan.json")
WORKOUT_FILE = Path(r"Data\Exercise\week_workout_plan.json")

# re_roll_meal(MEAL_PLAN_FILE, "Harissa Pasta")

# send_current_shopping_list(MEAL_PLAN_FILE)

# print(prev_weeks_last_gym_session(WORKOUT_FILE))