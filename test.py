from pathlib import Path

from shopping_list_generator import send_current_shopping_list, re_roll_meal
import Data.Mealplan.recipes as r

MEAL_PLAN_FILE = Path(r"Data\Mealplan\week_meal_plan.json")

# re_roll_meal(MEAL_PLAN_FILE, "Harissa Pasta")

send_current_shopping_list(MEAL_PLAN_FILE)