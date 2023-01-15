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



from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
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
    weight = Column(Integer)
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


""" Need to design db structure wrt ORM. """

  

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
