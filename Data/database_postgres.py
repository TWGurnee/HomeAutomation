import psycopg2 as sql
import random

from dataclasses import astuple
from pathlib import Path

from .Exercise import SessionType, MuscleGroup, Exercise, WorkoutSession, get_gym_config
from .Mealplan import Ingredient, Recipe


class Database(object):
    """sqlite3 database class for mealplan and exercise manipulation"""

    DB_NAME = Path(r"Data\database.db")
    conn = sql.connect(DB_NAME, check_same_thread=False) #TODO
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
        with open('schema.sql', "r") as f:
            script = f.read()
            cls.cursor.execute(script)

    @classmethod
    def clear_tables(cls):
        cls.cursor.execute("""
        DROP TABLE IF EXISTS ingredients;
        DROP TABLE IF EXISTS recipes;
        DROP TABLE IF EXISTS recipe_ingredients;
        DROP TABLE IF EXISTS exercises;
        """)
        cls.conn.commit()


    ## Helpers ###

    @classmethod
    def get_item_id(cls, table_name: str, item_name: str) -> int | None:
    
        if table_name == "ingredients":
            cls.cursor.execute("""
                SELECT ingredient_id
                FROM ingredients
                WHERE ingredient_name=?
                """, 
                (item_name,)
            )
            item_id = cls.cursor.fetchone()
            if not item_id:
                print(f"{item_name} not found in {table_name}")
                return

        if table_name == "recipes":
            cls.cursor.execute("""
                SELECT recipe_id
                FROM recipes
                WHERE recipe_name=?
                """, 
                (item_name,)
            )
            item_id = cls.cursor.fetchone()
            if not item_id:
                print(f"{item_name} not found in {table_name}")
                return            
            
        if table_name == "exercises":
            cls.cursor.execute("""
                SELECT exercise_id
                FROM exercises
                WHERE exercise_name=?
                """, 
                (item_name,)
            )
            item_id = cls.cursor.fetchone()
            if not item_id:
                print(f"{item_name} not found in {table_name}")
                return
            

        elif table_name not in ["ingredients", "recipes", "exercises"]:
            print("no table found of that name")
            return

        # Retrieve item_id int from tuple
        item_id = item_id[0] #type: ignore (possibly unbound error)

        return item_id
    

    ### Ingredients ###

    @classmethod
    def add_ingredient(cls, ingredient: Ingredient) -> None:
        name, quantity, category = astuple(ingredient)
        cls.cursor.execute("""
            INSERT INTO ingredients (ingredient_name,ingredient_shopping_category)
            VALUES (?, ?)""", (name, category,))
        cls.conn.commit()


    @classmethod
    def get_ingredients(cls):
        ingredients = cls.cursor.execute("SELECT ingredient_name, ingredient_shopping_category FROM ingredients")
        return [Ingredient(name=name, quantity=1, category=category) for name, category in ingredients]
    

    @staticmethod
    def get_ingredient_from_name(name: str):
        ingredients = {ingredient.name: ingredient for ingredient in Database.get_ingredients()} #type: ignore
        return ingredients.get(name)
    

    @classmethod # perhaps depreciated: get_item_id specifically queries and retrieves from database. This forces the entire list into the memory to search.
    def get_ingredient_id_from_name(cls, name: str):
        ingredients_table = list(cls.cursor.execute("SELECT * FROM ingredients"))
        id = {i[1]: i[0] for i in ingredients_table}
        return id.get(name)


    @staticmethod
    def categorise_ingredient(ingredient: str) -> str:
        """Get or assign category for a ingredient.name or string"""

        all_ingredients = Database.get_ingredients()

        # To get categories we need all current ingredients and their category.
        all_ingredient_names = [ingredient.name for ingredient in all_ingredients]
        get_category_from_name = {i.name: i.category for i in all_ingredients}

        # Categorise ingredient
        if ingredient in all_ingredient_names:
            category = get_category_from_name[ingredient]
        else:
            all_categories = {ingredient.category for ingredient in all_ingredients}
            category = input(f'Please choose food category from following:\n{all_categories}')

        return category


    ### Recipes ###

    @staticmethod
    def generate_recipe(recipe_dict: dict): #TODO: rework to take tuple of (category, name, [ingredients])
        """Helper method to generate recipes from a simple typed input dict:
        For example: 
        `Test_Recipe = {('Tim', 'Steak'): ['Steak', 'Broccoli/Asparagus', 'Chips/Potatoes', 'Peppercorn Sauce']}`
        `generate_recipe(Test_Recipe)`

        Currently result is unformatted and works on dicts of 1 recipe"""

        # Unpack input:
        meal_type, name = list(recipe_dict.keys())[0]
        ingredients = recipe_dict[(meal_type, name)]

        # Create list to hold the ingredients for building Recipe object.
        ingredient_objects = []

        # Fill ingredient_objects list
        for ingredient in ingredients:
            # Generic quantity value
            quantity = 1

            # Get category
            category = Database.categorise_ingredient(ingredient)

            # Add to list
            ingredient_objects.append(Ingredient(
                name=ingredient, quantity=quantity, category=category))

        return Recipe(name=name, ingredients=ingredient_objects, type=meal_type)


    @classmethod
    def add_recipe(cls, recipe: Recipe) -> None:
        """Adds a recipe to the recipe table and to the relating recipe_ingredients table"""        
        name, ingredients, type = astuple(recipe)

        cls.cursor.execute("""
            INSERT INTO recipes (recipe_name, recipe_type)
            VALUES (?, ?)""", (name, type,))
        
        recipe_id = cls.cursor.lastrowid
        recipe_ingredient_ids = [Database.get_item_id("ingredients", ingredient.name) for ingredient in ingredients]

        for ing_id in recipe_ingredient_ids:
            cls.cursor.execute("""
                INSERT INTO recipe_ingredients (ingredient_quantity, recipe_id, ingredient_id)
                VALUES (?, ?, ?)""",
                (1, recipe_id, ing_id)
            )

        cls.conn.commit()


    @classmethod
    def add_ingredient_to_recipe(cls, ingredient_name: str, recipe_name: str) -> None:
        ingredient_id = Database.get_item_id("ingredients", ingredient_name)
        recipe_id = Database.get_item_id("recipes", recipe_name)

        cls.cursor.execute("""
          INSERT INTO recipe_ingredients (ingredient_quantity, recipe_id, ingredient_id)
          VALUES (?, ?, ?)""",
          (1, recipe_id, ingredient_id)
        )

        cls.conn.commit()


    @classmethod
    def get_recipes(cls, limit: str=None) -> list[Recipe]: # type: ignore
        """Returns list of all recipes with optional specifier argument. Can return the names only or specified categories. """

        cls.cursor.execute("""
        SELECT r.recipe_name, r.recipe_type, i.ingredient_name, ri.ingredient_quantity, i.ingredient_shopping_category
        FROM recipes r
        JOIN recipe_ingredients ri ON r.recipe_id = ri.recipe_id
        JOIN ingredients i ON i.ingredient_id = ri.ingredient_id
        """)
        
        rows = cls.cursor.fetchall()
        
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
    def get_recipe_from_name(name: str) -> Recipe:
        meals_dict = {meal.name: meal for meal in Database.get_recipes()} #type: ignore
        return meals_dict.get(name) #type: ignore
    


    ### Exercises ###

    @staticmethod
    def get_exercises(selection: SessionType=None) -> list[Exercise]: #type: ignore
        """Returns list of all exercises unless SessionType specified. """

        exercises = list(Database.cursor.execute("SELECT * FROM exercises"))
        if not selection:
            return [
                Exercise(name=name, type=type, muscle_group=muscle_group, weight=weight, weight_increment=weight_increment, reps=reps, time=time, secondary_type=secondary_type)
                for id, name, type, secondary_type, muscle_group, weight, weight_increment, reps, time in exercises
                ]
        
        elif selection == SessionType.UPPER:
            return [
                Exercise(name=name, type=type, muscle_group=muscle_group, weight=weight, weight_increment=weight_increment, reps=reps, time=time, secondary_type=secondary_type)
                for id, name, type, secondary_type, muscle_group, weight, weight_increment, reps, time in exercises
                if muscle_group in [
                    MuscleGroup.UPPER_BACK.value,
                    MuscleGroup.CHEST_PRESS.value,
                    MuscleGroup.CHEST_FLY.value,
                    MuscleGroup.SHOULDER_PRESS.value,
                    MuscleGroup.SHOULDER_SIDE.value,
                    MuscleGroup.BICEP.value,
                    MuscleGroup.TRICEP.value
                ]
                and type != SessionType.HIIT.value
            ]

        elif selection == SessionType.LOWER:
            return [
                Exercise(name=name, type=type, muscle_group=muscle_group, weight=weight, weight_increment=weight_increment, reps=reps, time=time, secondary_type=secondary_type)
                for id, name, type, secondary_type, muscle_group, weight, weight_increment, reps, time in exercises
                if muscle_group in [
                    MuscleGroup.CORE.value,
                    MuscleGroup.LOWER_BACK.value,
                    MuscleGroup.WHOLE_LEG.value,
                    MuscleGroup.QUADS.value,
                    MuscleGroup.HAMSTRINGS.value,
                    MuscleGroup.GLUTES.value
                ]
                and type != SessionType.HIIT.value
            ]

        else: 
            return [
                Exercise(name=name, type=type, muscle_group=muscle_group, weight=weight, weight_increment=weight_increment, reps=reps, time=time, secondary_type=secondary_type)
                for id, name, type, secondary_type, muscle_group, weight, weight_increment, reps, time in exercises
                if type == selection.value
            ]
        
                

### random generation functions ###

def generate_exercise_session_by_type(day_type: SessionType) -> dict: #type: ignore
    """Returns a set of random exercises depending on the SessionType given."""
    exercises = []
    GYM_INDEXES, WEEK_ALLOWANCES, GYM_DAY_CONFIG = get_gym_config() # type: ignore

    if day_type == SessionType.CARDIO:

        exercises.extend(random.sample(Database.get_exercises(SessionType.CARDIO), 1))
        
        return{day_type.value: exercises}

    else:       
        for muscle_group, exercise_number in GYM_DAY_CONFIG.get(day_type): #type: ignore
            exercise_list = Database.get_exercises(day_type)
            exercises.extend(WorkoutSession.grab_selection(exercise_list, muscle_group, exercise_number))


        return {day_type.value: exercises}


def get_workout_session(day_type: SessionType) -> WorkoutSession:
    """Returns a workout session with random exercises depending on the SessionType given."""
    exercises = []
    GYM_INDEXES, WEEK_ALLOWANCES, GYM_DAY_CONFIG = get_gym_config() # type: ignore

    if day_type == SessionType.CARDIO:

        exercises.extend(random.sample(Database.get_exercises(SessionType.CARDIO), 1))
        
        return WorkoutSession(name=day_type.value, exercises=exercises, exercise_type=day_type)

    else:       
        for muscle_group, exercise_number in GYM_DAY_CONFIG.get(day_type): #type: ignore
            exercise_list = Database.get_exercises(day_type)
            exercises.extend(WorkoutSession.grab_selection(exercise_list, muscle_group, exercise_number))

        return WorkoutSession(name=day_type.value, exercises=exercises, exercise_type=day_type)


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
    
    return {"HIIT workout": plan}
    # return WorkoutSession(name="HIIT workout", exercises=plan, exercise_type=SessionType.HIIT)


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
