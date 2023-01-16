import sqlite3 as db
from pathlib import Path

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



from sqlalchemy import Column, Integer, String, Float, ForeignKey, Table, create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Ingredient(Base):
    __tablename__ = 'ingredient'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    quantity = Column(Integer)
    category = Column(String)
    
class Recipe(Base):
    __tablename__ = 'recipe'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    ingredients = relationship("Ingredient")

class Exercise(Base):
    __tablename__ = 'exercise'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String, ForeignKey('session_type.name'))
    muscle_group = Column(String, ForeignKey('muscle_group.name'))
    weight = Column(Float)
    #weight_increment = Column(Float)
    #weeks_target_reached = Column(Integer)
    reps = Column(Integer)
    time = Column(Integer)
    secondary_type = Column(String, ForeignKey('session_type.name'))

class SessionTypeModel(Base):
    __tablename__ = 'session_type'
    name = Column(String, primary_key=True)

class MuscleGroupModel(Base):
    __tablename__ = 'muscle_group'
    name = Column(String, primary_key=True)

class WorkoutSession(Base):
    __tablename__ = 'workout_session'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String, ForeignKey('session_type.name'))
    exercises = relationship("Exercise")
    muscle_groups = relationship("MuscleGroupModel")


 
# To create a interactive db with front end inputs we need a bool check to see if all sets were completed at the target weight. 
# If weight drops then we keep the same weight. 
# If reps drop we keep the same weight.
# If target is hit for 2/3/4 weeks then we add some weight.

# Therefore, variables needed for exercise:
    # target_hit: boolean - replace with backend function to update DB weeks_target_reached.
    # weight_increment: float

# Questions:
    # Do we save a completed workout as a single instance separate to the relational DB Exercise?
    # If so each completed would have the target reached tickbox, whereas the actual excercise may not
    # Can have a function to (batch?) check the DB to ensure if completed workouts have checked targets that the DB field in exercise is upped by the weight increment.
    # Can save the need for multiple weeks to be saved if this DB saves the number of weeks hit the target in a row
    # This would then be included within the Exercise table?

# DB model needed to save all data from completed workout:
    # class CompletedWorkouts(Base):
        # __tablename__ = 'completed workouts'
        # date = Column(datetime)
        # workoutsession = relationship("WorkoutSession") #TODO decidce which is needed this or below VV
        # exercises = relationship("Exercise") **** Here would we create a snapshot of the weights completed at the time - could use for stats and progression. 


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# # create a connection to the database
# engine = create_engine('sqlite:///exercises_recipes.db')

# # create all the tables defined in the models
# Base.metadata.create_all(engine)

# # create a session factory
# Session = sessionmaker(bind=engine)

# # create a new session and add the exercises and recipes to the database
# session = Session()

# # exercises and recipes are list of Exercises and Recipe objects
# for exercise in exercises:
#     session.add(exercise)

# for recipe in recipes:
#     session.add(recipe)

# # commit the changes
# session.commit()
# session.close()





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
