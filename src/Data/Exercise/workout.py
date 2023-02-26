import random

from dataclasses import dataclass, field

from .exercise import Exercise
from .session_type import SessionType
from .muscle_group import MuscleGroup


@dataclass
class WorkoutSession:
    name: str
    exercises: list[Exercise] = field(default_factory=list)
    exercise_type: SessionType = field(default=None) #type: ignore
    muscle_groups: list[MuscleGroup] = field(default=None) #type: ignore

    ### Init methods ###
    @staticmethod
    def init_all_exercises(list_of_exercises: list[Exercise]):
        return WorkoutSession("All Exercises", exercises=list_of_exercises)

    @staticmethod
    def get_exercises_by_type(all_exercises, exercise_type: SessionType) -> list[Exercise]:
        return [exercise for exercise in all_exercises.exercises if exercise.type == exercise_type]

    @staticmethod
    def init_workout_by_type(all_exercises, exercise_type: SessionType):
        name=exercise_type.value
        exercises = WorkoutSession.get_exercises_by_type(all_exercises, exercise_type)
        return WorkoutSession(name, exercises=exercises, exercise_type=exercise_type)


    ### Workout Generation Methods ###
    @staticmethod
    def grab_selection(exercise_list: list[Exercise], muscle_group: MuscleGroup, number: int) -> list[Exercise]:
        """Returns a random selection exercises. The muscle group and number of exercises returned are entered as arguments"""
        return random.sample([e for e in exercise_list if e.muscle_group == muscle_group.value], number)
    

    def to_plan(self):
        return {self.name: self.exercises}
    

    ### Helper methods ###
    def add_exercise(self, exercise: Exercise):
        self.exercises.append(exercise)

    def add_exercises(self, list_of_exercises: list[Exercise]):
        self.exercises.extend(list_of_exercises)

    def remove_exercise(self, exercise: Exercise):
        self.exercises.remove(exercise)


    ### Unfinished/Unused methods ###
    @staticmethod
    def to_string(session: "WorkoutSession") -> str:
        ...
        
    @staticmethod
    def move_exercise(exercise: Exercise, from_workout_type, to_workout_type): 
        """Function for moving an exercise between workouts"""
        # Ideally this could be utilised within the front end; once the database is in use.
        # This may not be needed as the schema can just be updated backend in the construction of the backed datatypes
        pass


