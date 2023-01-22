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


    ### Initialisation of Database ###

    @classmethod
    def init_tables(cls):
        with open('schema.sql') as f:
            script = f.read()
            cls.conn.executescript(script)


    ### Filling Tables ###

    # @classmethod
    # def fill_ingredients(cls):
    #     for ingredient in Ingredient.All_Ingredients:
    #         name, quantity, category = astuple(ingredient)
    #         cls.cursor.execute("""
    #             INSERT INTO ingredients (ingredient_name,ingredient_shopping_category)
    #             VALUES (?, ?)""", (name, category,))
    #     cls.conn.commit()


    # @classmethod
    # def fill_recipes(cls):
    #     for recipe in Recipe.All_Recipes:
    #         name, ingredients, type = astuple(recipe)
    #         cls.cursor.execute("""
    #             INSERT INTO recipes (recipe_name, recipe_type)
    #             VALUES (?, ?)""", (name, type,))
    #     cls.conn.commit()


    # @classmethod
    # def fill_recipe_ingredients(cls):
    #     recipes_table = list(cls.cursor.execute("SELECT * FROM recipes"))
    #     ingredients_table = list(cls.cursor.execute("SELECT * FROM ingredients"))

    #     def get_ingredient_id_from_name(name):
    #         id = {i[1]: i[0] for i in ingredients_table}
    #         return id.get(name)

    #     for id, name, category in recipes_table:
    #         # get ingredients from recipe
    #         recipe = Recipe.get_recipe_from_name(name)
    #         recipe_id = id
    #         recipe_ingredient_ids = [get_ingredient_id_from_name(i.name) for i in recipe.ingredients] # type: ignore

    #         for ing_id in recipe_ingredient_ids:

    #             cls.cursor.execute("""
    #                 INSERT INTO recipe_ingredients (ingredient_quantity, recipe_id, ingredient_id)
    #                 VALUES (?, ?, ?)""",
    #                 (1, recipe_id, ing_id)
    #             )
    #     cls.conn.commit()


    @classmethod
    def fill_exercises(cls):
        for exercise in ALL_EXERCISES.exercises:
            name, type, muscle_group, weight, reps, time, secondary_type = exercise.to_tuple()
            cls.conn.execute("""
                INSERT INTO exercises (exercise_name,exercise_type,exercise_secondary_type,exercise_musclegroup,exercise_weight,exercise_reps,exercise_time)
                VALUES (?, ?, ?, ?, ?, ?, ?)""", (name, type, secondary_type, muscle_group, weight, reps, time,))
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
    def get_exercises(selection: SessionType=None) -> list(Exercise): #type: ignore
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
