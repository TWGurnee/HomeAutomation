import sqlite3 as db
from pathlib import Path
from dataclasses import astuple

from Exercise.exercise import *
from Mealplan.recipes import *


class Database(object):
    """sqlite3 database class for mealplan and exercise manipulation"""

    DB_NAME = Path(r"database.db") #TODO Move to `YAML` config file to ensure secure.
    conn = db.connect(DB_NAME)
    cursor = conn.cursor()

    ### Context manager functions ###
    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

    @classmethod
    def init_tables(cls):
        with open('schema.sql') as f:
            script = f.read()
            cls.conn.executescript(script)

    @classmethod
    def fill_ingredients(cls):
        for ingredient in Ingredient.All_Ingredients:
            name, quantity, category = astuple(ingredient)
            cls.conn.execute("""
                INSERT INTO ingredients (ingredient_name,ingredient_shopping_category)
                VALUES (?, ?)""", (name, category,))
            
    @classmethod
    def fill_exercises(cls):
        for exercise in ALL_EXERCISES.exercises:
            name, type, muscle_group, weight, reps, time, secondary_type = exercise.to_tuple()
            cls.conn.execute("""
                INSERT INTO exercises (exercise_name,exercise_type,exercise_secondary_type,exercise_musclegroup,exercise_weight,exercise_reps,exercise_time)
                VALUES (?, ?)""", (name, type, secondary_type, muscle_group, weight, reps, time))

# Database.init_tables()

with Database() as base:
    res = base.conn.execute("SELECT ingredient_name FROM ingredients")
    print(res.fetchall())

# Database.fill_exercises()


    # TODO
    # Workout table?
    # Exercise Workout join table?


    
    ### Initialisation methods ###
    
    # Fill exercises
    # Fill recipes

    ### Helper functions ###

    ### Data manipulation methods ###
    
    ## Recipes
    # Add a Recipe
    # Add item to recipe
    # Remove item from recipe
    # Generate Meal Plan
    # Get recipe from name
    # Get all recipes?
    
    ## Exercise
    # Add an exercise
    # Change an exercises day type
    # Add an input weight
    # Add an input reps


### Queries ###

# To work with queries we need values from written classes as tuples.