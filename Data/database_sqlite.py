import sqlite3 as sql
from pathlib import Path
from dataclasses import astuple

from Exercise.exercise import *
from Mealplan.recipes import *


class Database(object):
    """sqlite3 database class for mealplan and exercise manipulation"""

    DB_NAME = Path(r"database.db") #TODO Move to `YAML` config file to ensure secure.
    conn = sql.connect(DB_NAME)
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
        cls.conn.commit()


    @classmethod
    def fill_recipes(cls):
        for recipe in Recipe.All_Recipes:
            name, ingredients, type = astuple(recipe)
            cls.conn.execute("""
                INSERT INTO recipes (recipe_name, recipe_type)
                VALUES (?, ?)""", (name, type,))
        cls.conn.commit()

    @classmethod
    def fill_recipe_ingredients(cls):
        recipes = cls.cursor.execute("SELECT * FROM recipes")
        for i in recipes: print(i)


    @classmethod
    def fill_exercises(cls):
        for exercise in ALL_EXERCISES.exercises:
            name, type, muscle_group, weight, reps, time, secondary_type = exercise.to_tuple()
            cls.conn.execute("""
                INSERT INTO exercises (exercise_name,exercise_type,exercise_secondary_type,exercise_musclegroup,exercise_weight,exercise_reps,exercise_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)""", (name, type, secondary_type, muscle_group, weight, reps, time,))
        cls.conn.commit()


# Database.init_tables()

Database.fill_recipe_ingredients()

# with Database() as base:
#     res = base.conn.execute("SELECT ingredient_name FROM ingredients")
#     print(res.fetchall())


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