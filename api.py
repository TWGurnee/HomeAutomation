from flask import Flask, request
import requests as req
import threading as td

import shopping_list as shop_list
import Data.recipes as meals
from scheduler import scheduler

def start_scheduler_thread():
    """Starts email scheduler prior to api."""
    print('hi')
    schedule = td.Thread(target=scheduler, daemon=True)
    schedule.start()


api = Flask(__name__)

start_scheduler_thread()

@api.route('/update-shopping-list', methods=['GET', 'POST'])
def update_shopping_list():
    """API endpoint for updating the shopping list"""

    MEAL_PLAN_FILE = r"Data\ingredients.json"
    
    if request.method == 'POST': # Request from Alexa with list to update local list.
        
        # Receive items in payload, #TODO: extract data into list of strings
        items = req.json('item')

        # Assign variable of current local machine meal plan
        data = shop_list.get_last_weeks_meal_plan(MEAL_PLAN_FILE)

        # Extract ingredients_by_category dict
        meal_plan = data['Meal Plan']
        shopping_list = data['Shopping List']

        # Categorise items
        item_list = []
        for item in items:
            # Get category
            category = meals.categorise_ingredient(item)

            # Add to list
            item_list.append(meals.Ingredient(name=item, quantity=1, category=category))
        
        for item in item_list:
           shop_list.update_ingredients_by_category(item, shopping_list)

        shop_list.save_new_meal_plan(MEAL_PLAN_FILE, meal_plan, shopping_list)

    
    if request.method == 'GET': # Request from Alexa to pull a new shopping list from the weekly meal plan.

        data = shop_list.get_last_weeks_meal_plan()





### run ###
if __name__ == '__main__':
    api.run(host='127.168.0.50')
