import sqlite3 as db
from pathlib import Path
from dataclasses import astuple

import Exercise.exercise as e
import Mealplan.recipes as r


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


    def init_tables(self):
        with open('schema.sql') as f:
            self.conn.executescript(f.read())


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