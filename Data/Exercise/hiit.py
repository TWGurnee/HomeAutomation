import random

from dataclasses import dataclass
from copy import deepcopy


from .session_type import SessionType
from .exercise import Exercise
from .workout import HIIT_EXERCISES


@dataclass
class HIIT:
    type: SessionType
    exercises: list[Exercise]

    @staticmethod
    def _get_plan():
        """Randomly generates a plan for a HIIT workout.
        Fills up to 15 exercises, to be done in a 30 active and 30 second rest.
        2 sets would provide a 30 minute workout."""

        #first copy the list of HIIT Exercises for use.
        exercise_pool = deepcopy(HIIT_EXERCISES)

        # Prev muscle_group to be stored for checks.
        prev_exercise_type = None

        # Loop counter to prevent infinity looping.
        loops = 0

        # Initialise list for plan to be filled by loop below.
        plan = []

        # Start plan filling:
        while len(plan) != 15:

            # Loop breaker if infinite loop caused.
            if loops > 30:
                return {"HIIT workout": plan}

            # Pick HIIT exercise
            chosen_exercise = random.choice(exercise_pool)

            # If the muscle group of the exercise is same as prev; discard.
            if chosen_exercise.muscle_group == prev_exercise_type:
                loops+=1
                continue
            
            else:
                # Add new exercise to plan.
                plan.append(chosen_exercise)
                # Set the MuscleGroup to ensure no muscle overload.
                prev_exercise_type = chosen_exercise.muscle_group
                # Remove exercise from pool to ensure isnt duplicated.
                exercise_pool.remove(chosen_exercise)
        
        return {"HIIT workout": plan} #TODO - timings?