import sqlite3 as sql
import random

from pathlib import Path

from .Exercise import SessionType, MuscleGroup, Exercise, WorkoutSession, GYM_DAY_CONFIG

from .Mealplan import Ingredient, Recipe


class Database(object):
    """sqlite3 database class for mealplan and exercise manipulation"""

    DB_NAME = Path(r"Data\database.db")
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


    ### Initialisation of Database ###

    @classmethod
    def init_tables(cls):
        with open('schema.sql') as f:
            script = f.read()
            cls.conn.executescript(script)

    @classmethod
    def clear_tables(cls):
        cls.conn.execute("""
        DROP TABLE IF EXISTS ingredients;
        DROP TABLE IF EXISTS recipes;
        DROP TABLE IF EXISTS recipe_ingredients;
        DROP TABLE IF EXISTS exercises;
        """)
        cls.conn.commit()


    ### Retrieval ###

    @staticmethod
    def get_ingredients():
        ingredients = Database.cursor.execute("SELECT ingredient_name, ingredient_shopping_category FROM ingredients")
        return [Ingredient(name=name, quantity=1, category=category) for name, category in ingredients]
    

    @staticmethod
    def get_recipes(limit: str=None): # type: ignore
        """Returns list of all recipes with optional specifier argument. Can return the names only or specified categories. """

        Database.cursor.execute("""
        SELECT r.recipe_name, r.recipe_type, i.ingredient_name, ri.ingredient_quantity, i.ingredient_shopping_category
        FROM recipes r
        JOIN recipe_ingredients ri ON r.recipe_id = ri.recipe_id
        JOIN ingredients i ON i.ingredient_id = ri.ingredient_id
        """)
        
        rows = Database.cursor.fetchall()
        
        recipes = {}

        for row in rows:
            recipe_name = row[0]

            if recipe_name not in recipes:
                recipes[recipe_name] = Recipe(name=recipe_name, ingredients=[], type=row[1])

            ingredient = Ingredient(name=row[2], quantity=row[3], category=row[4])

            recipes[recipe_name].ingredients.append(ingredient)

        if not limit:
            return list(recipes.values())
        
        elif limit == "Name" or "name" or "Names" or "names":
            return list(recipes.keys())
        
        elif limit in ["Tim", "Freya", "Healthy"]:
            return [r for r in list(recipes.values()) if r.type == limit]
    

    @staticmethod
    def get_exercises(selection: SessionType=None) -> list[Exercise]: #type: ignore
        """Returns list of all exercises unless SessionType specified. """

        exercises = list(Database.cursor.execute("SELECT * FROM exercises"))
        if not selection:
            return [
                Exercise(name=name, type=type, muscle_group=muscle_group, weight=weight, reps=reps, time=time, secondary_type=secondary_type)
                for id, name, type, secondary_type, muscle_group, weight, weight_increment, reps, time in exercises
                ]
        
        else: 
            return [
                Exercise(name=name, type=type, muscle_group=muscle_group, weight=weight, reps=reps, time=time, secondary_type=secondary_type)
                for id, name, type, secondary_type, muscle_group, weight, weight_increment, reps, time in exercises
                if type == selection.value
            ]
        

### random generation functions ###

def generate_exercise_session_by_type(day_type: SessionType) -> dict: #type: ignore
    """Returns a set of random exercises depending on the SessionType given."""
    exercises = []

    if day_type == SessionType.CARDIO:

        exercises.extend(random.sample(Database.get_exercises(SessionType.CARDIO), 1))
        
        return{day_type.value: exercises}

    else:       
        for muscle_group, exercise_number in GYM_DAY_CONFIG.get(day_type): #type: ignore
            exercise_list = Database.get_exercises(day_type)
            exercises.extend(WorkoutSession.grab_selection(exercise_list, muscle_group, exercise_number))
     
        return {day_type.value: exercises}


def generate_HIIT_plan():
    """Randomly generates a plan for a HIIT workout.
    Fills up to 15 exercises, to be done in a 30 active and 30 second rest.
    2 sets would provide a 30 minute workout."""

    exercise_pool = Database.get_exercises(SessionType.HIIT)

    prev_exercise_type = None
    # Loop counter to prevent infinity looping.
    loops = 0
    # Initialise list for plan to be filled by loop below.
    plan = []

    while len(plan) != 15:

        if loops > 30:
            return {"HIIT workout": plan}

        chosen_exercise = random.choice(exercise_pool)

        if chosen_exercise.muscle_group == prev_exercise_type:
            loops+=1
            continue
        
        else:
            plan.append(chosen_exercise)
            # Set the MuscleGroup to ensure no muscle overload.
            prev_exercise_type = chosen_exercise.muscle_group
            # Remove exercise from pool to ensure isnt duplicated.
            exercise_pool.remove(chosen_exercise)
    
    return {"HIIT workout": plan} #TODO - timings?


# Database.init_tables()


    # TODO
    # Workout table?
    # Exercise Workout join table?


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
