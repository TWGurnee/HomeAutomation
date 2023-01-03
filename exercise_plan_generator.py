import json

from pathlib import Path

from Data.Exercise.exercises import *

### Functions ###

def choose_exercises(day_type: SessionType) -> dict: #type: ignore #TODO refactor list comprehensions into WorkoutSession staticmethod to simplify look
    """Returns a set of random exercises depending on the SessionType given."""
    if day_type == SessionType.BACK_CORE_ARMS:
        exercises = []
        
        #back
        exercises.extend(random.sample([e for e in Exercise.Back_Core_Arm_Day if e.muscle_group == MuscleGroup.UPPER_BACK], 2))
        exercises.extend(random.sample([e for e in Exercise.Back_Core_Arm_Day if e.muscle_group == MuscleGroup.LOWER_BACK], 1))
        #core
        exercises.extend(random.sample([e for e in Exercise.Back_Core_Arm_Day if e.muscle_group == MuscleGroup.CORE], 1))
        #arms
        exercises.extend(random.sample([e for e in Exercise.Back_Core_Arm_Day if e.muscle_group == MuscleGroup.BICEP], 2))
        exercises.extend(random.sample([e for e in Exercise.Back_Core_Arm_Day if e.muscle_group == MuscleGroup.TRICEP], 2))
        
        return {"Back Core Arm day": exercises}

    elif day_type == SessionType.CHEST_SHOULDERS:
        exercises = []
        
        #chest
        exercises.extend(random.sample([e for e in Exercise.Chest_Shoulder_Day if e.muscle_group == MuscleGroup.CHEST_PRESS], 3))
        exercises.extend(random.sample([e for e in Exercise.Chest_Shoulder_Day if e.muscle_group == MuscleGroup.CHEST_FLY], 1))
        #shoulder
        exercises.extend(random.sample([e for e in Exercise.Chest_Shoulder_Day if e.muscle_group == MuscleGroup.SHOULDER_PRESS], 2))
        exercises.extend(random.sample([e for e in Exercise.Chest_Shoulder_Day if e.muscle_group == MuscleGroup.SHOULDER_SIDE], 2))
        
        return {"Chest Shoulder day": exercises}
    
    elif day_type == SessionType.LEGS:
        exercises = []

        #whole leg
        exercises.extend(random.sample([e for e in Exercise.Leg_Day if e.muscle_group == MuscleGroup.WHOLE_LEG], 3))
        #quads
        exercises.extend(random.sample([e for e in Exercise.Leg_Day if e.muscle_group == MuscleGroup.QUADS], 1))
        #hammys
        exercises.extend(random.sample([e for e in Exercise.Leg_Day if e.muscle_group == MuscleGroup.HAMSSTRINGS], 1))
        #glutes
        exercises.extend(random.sample([e for e in Exercise.Leg_Day if e.muscle_group == MuscleGroup.GLUTES], 1))

        return {"Leg day": exercises}

    elif day_type == SessionType.CARDIO:
        exercises = []
        
        #cardio
        exercises.extend(random.sample(Exercise.Cardio, 1))
        
        return{"Cardio day": exercises}


def get_exercise_sessions(WEEK_ALLOWANCES: dict) -> list[dict]:
    """Returns list of exercises to be done in the week."""
    exercise_sessions = []

    for session_type, allowance in WEEK_ALLOWANCES.items():

        if session_type == SessionType.REST: 
            pass
         
        else:
            for _ in range(allowance):
                exercise_sessions.append(choose_exercises(session_type))

    return exercise_sessions


def fill_weekly_plan(week_days: list[str], exercise_sessions: list[dict]) -> dict:

    #Initialise weekly plan for filling:
    exercise_plan = {
        'Monday': {},
        'Tuesday': {},
        'Wednesday': {},
        'Thursday': {},
        'Friday': {},
        'Saturday': {},
        'Sunday': {}
    }

    # To allow for a day gap between each gym session, below are all possible configurations indexes of the week.
    gym_indexes = [
        [0,2,4],
        [0,2,5],
        [0,2,6],
        [0,3,5],
        [0,3,6],
        [0,4,6],
        [1,3,5],
        [1,3,6],
        [1,4,6],
        [2,4,6]
    ]

    # Choose the gym day indexes from the list at random
    gym_day_indexes = random.choice(gym_indexes)

    # List the gym days
    gym_pass = [
        "Back Core Arm day",
        "Chest Shoulder day",
        "Leg day"
    ]

    # Create list of the randomised gym days from all of the weekly plan
    gym_sessions = [session for session in exercise_sessions if list(session.keys())[0] in gym_pass]

    # Shuffle the list to ensure variety #TODO: Consider if stability in muscle groups is better for rest/recovery.
    random.shuffle(gym_sessions)

    ### Pass one: Assigning gym days 
    for index, session in zip(gym_day_indexes, gym_sessions):
        # Select the day of the week
        chosen_day = week_days[index]
        # Inert into exercise_plan dict
        exercise_plan[chosen_day] = session


    ### Pass Two: Assigning Rest days
    # We want the non-gym days: grab remaining indexes
    remaining_indexes = [i for i in range(7) if i not in gym_day_indexes]
    # Choose random rest day indexes
    rest_day_indexes = random.sample(remaining_indexes, 2)

    # Assign rest days as above:
    for index in rest_day_indexes:
        chosen_day = week_days[index]
        exercise_plan[chosen_day] = {"Rest day": []}

    ### Pass Three:
    # Finally we account for the Cardio exercises:

    # Need variable to extract the chosen cardio exercises
    cardio_pass = "Cardio day"
    # List of the chosen cardio exercises:
    cardio_sessions = [session for session in exercise_sessions if list(session.keys())[0] is cardio_pass]
    random.shuffle(cardio_sessions)

    # Get the remaining gaps in the schedule:
    final_indexes = [i for i in range(7) if i not in gym_day_indexes and i not in rest_day_indexes]

    # Iterate through the sessions to add accordingly:
    for session in cardio_sessions:
        # Grab out the exercise from the dict for analysis:
        exercise = session['Cardio day'][0]

        # If session is a HIIT, update session to be full plan.
        if exercise.secondary_type == SessionType.HIIT:
            session = HIIT._get_plan()

        # As the plan can be filled, we need to account for situations where we have a cardio session left to add:
        if not final_indexes:
            if not exercise.secondary_type:
                # Sometimes we get lucky and have less cardio in a week.

                # This could be updated in future to swap in to a previous cardio day if it has a secondary_type.
                # Or if not to just have one less Rest day.
                # But let's start easy for now.  
                pass
            
            # 5K's have a REST secondary type; We can do a restful jog for 30 mins to aid recovery
            if exercise.secondary_type == SessionType.REST:
                index = random.choice(rest_day_indexes)
                chosen_day = week_days[index]
                rest_day_to_update = exercise_plan[chosen_day]
                rest_day_to_update["Rest day"].append(exercise)

            # A HIIT is best done in the gym; therefore if left over we can include within a gym day:
            if exercise.secondary_type == SessionType.HIIT:
                index = random.choice(gym_day_indexes)
                chosen_day = week_days[index]
                exercise_plan[chosen_day].update(session)

        # If no negative criteria are met, add the cardio exercise to the plan
        else: 
            # Get first index:     
            index = final_indexes[0]
            # Get the day of the index:
            chosen_day = week_days[index]
            # Add session to the week plan:
            exercise_plan[chosen_day] = session
            # Remove index to ensure next cardio exercise is added to next free day
            final_indexes.remove(index)


    return exercise_plan


def save_new_plan(exercise_plan: dict, SAVE_LOCATION):
    with open(SAVE_LOCATION, 'w') as f:
        data = {}
        for day, session in exercise_plan.items():
            output = {}
            session_type = list(session.keys())[0]
            exercises = list(session.values())[0]

            output[session_type] = [Exercise.to_dict(exercise) for exercise in exercises]

            data[day] = [output]
            
        json.dump(data, f)

def load_current_plan(SAVE_LOCATION):
    with open(SAVE_LOCATION, 'r') as f:
        return json.load(f)

###################################~~~MAIN~~~####################################
### CONSTANTS ###

week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Week consists of: { Type of workout session: number of weekdays}
WEEK_ALLOWANCES = {
    SessionType.BACK_CORE_ARMS: 1,
    SessionType.CHEST_SHOULDERS: 1,
    SessionType.LEGS: 1,
    SessionType.CARDIO: 3,
    SessionType.REST: 2
}

SAVE_LOCATION = Path.cwd() / r"Data\Exercise\workouts.json"


if __name__ == '__main__':
    exercise_sessions = get_exercise_sessions(WEEK_ALLOWANCES)

    exercise_plan = fill_weekly_plan(week_days, exercise_sessions)

    # Print checks:

    # for j, i in zip(exercise_plan.keys(), exercise_plan.values()):
    #     print(f'{j}: {list(i.items())}')

    save_new_plan(exercise_plan, SAVE_LOCATION)