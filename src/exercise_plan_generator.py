import json
import random
import datetime

from pathlib import Path

from .Data.Exercise import SessionType, Exercise, WorkoutSession, get_gym_config
from .Data.database_sqlite import generate_exercise_session_by_type, generate_HIIT_plan
from .Data.helpers import load_current_plan

### Functions ###

def get_exercise_sessions(WEEK_ALLOWANCES: dict) -> list[dict]:
    """Returns list of exercises to be done in the week."""
    exercise_sessions = []

    for session_type, allowance in WEEK_ALLOWANCES.items():

        if session_type == SessionType.REST: 
            pass
        
        else:
            for _ in range(allowance):
                exercise_sessions.append(generate_exercise_session_by_type(session_type))

    return exercise_sessions


def prev_weeks_last_gym_session(EXERCISE_PLAN_SAVE, gym_config) -> str: #type: ignore
    """Return the name of the last gym workout in the previous week"""
    
    plan = load_current_plan(EXERCISE_PLAN_SAVE)
    
    sessions = list(plan.values())
    
    # Will iterate through list back to front to return once first match found.
    sessions.reverse()

    gym_days = list(gym_config.keys())
    
    gym_pass = [day.value for day in gym_days]

    for session in sessions:
        session = session[0]
        session_title = list(session.keys())[0] 
        if session_title in gym_pass:
            return session_title


def current_weekly_workout_plan_for_dash(EXERCISE_PLAN_SAVE):

    plan = load_current_plan(EXERCISE_PLAN_SAVE)
    days = list(plan.keys())
    sessions = [session[0] for session in list(plan.values())]

    workout_sessions = [WorkoutSession(name=list(session.keys())[0], exercises=list(session.values())[0]) for session in sessions]

    return (days, workout_sessions)



def simplified_weekly_workout_plan(EXERCISE_PLAN_SAVE):

    plan = load_current_plan(EXERCISE_PLAN_SAVE)
    days = list(plan.keys())
    sessions = [list(session[0])[0] for session in list(plan.values())]
    exercises = [session[0] for session in list(plan.values())]
    exercises = [list(e.values())[0] for e in exercises]
    exercises = [[i.get("name") for i in e] if e else "Rest" for e in exercises]

    return (days, sessions, exercises)


def fill_weekly_plan(week_template: dict,
                     gym_config: dict,
                     gym_indexes: list[list[int]],
                     last_gym_session: str,
                     exercise_sessions: list[dict]) -> dict:
    
    """fills with a weekly template with a randomised weekly exercise plan"""

    # To allow for a day gap between each gym session, below are all possible configurations indexes of a 3 day week.
    # gym_indexes = [
    #     [0,2,4],
    #     [0,2,5],
    #     [0,2,6],
    #     [0,3,5],
    #     [0,3,6],
    #     [0,4,6],
    #     [1,3,5],
    #     [1,3,6],
    #     [1,4,6],
    #     [2,4,6]
    # ]

    # Choose the gym day indexes from the list at random
    gym_day_indexes = random.choice(gym_indexes)

    # List the gym days
    gym_days = list(gym_config.keys())
    gym_pass = [day.value for day in gym_days]
    
    # gym_pass = [
    #     "Back Core Arm day",
    #     "Chest Shoulder day",
    #     "Leg day"
    # ]

    # OR

    # gym_pass = [
    #     "Upper Body",
    #     "Upper Body",
    #     "lower Body",
    #     "lower Body"
    # ]


    # Create list of the randomised gym days from all of the weekly plan
    gym_sessions = [session for session in exercise_sessions if list(session.keys())[0] in gym_pass]

    # Randomise order if 3 day plan
    if len(gym_sessions) == 3:
        random.shuffle(gym_sessions)

    #Helper function in-case we have back to back gym sessions of the same type.
    def replace_first_session(gym_sessions):
        """Moves first session to a random other position in the list."""
        first_session = gym_sessions[0]
        x = len(gym_sessions)
        gym_sessions.remove(first_session)
        gym_sessions.insert(random.choice([x-1, x-2]), first_session)

    # Check if first in sessions is same as last gym session completed, and if so alter list
    first_session = gym_sessions[0]
    first_session_title = list(first_session.keys())[0]
    if first_session_title == last_gym_session:
        replace_first_session(gym_sessions)

    
    # If 4 day week we want alternating days: (upper, lower, upper, lower)
    elif len(gym_sessions) == 4:
        second_upper = gym_sessions[1]
        gym_sessions.remove(second_upper)
        gym_sessions.insert(2, second_upper)


    ### Pass one: Assigning gym days 
    for index, session in zip(gym_day_indexes, gym_sessions):
        # Select the day of the week
        chosen_day = list(week_template)[index]
        # Insert into exercise_plan dict
        week_template[chosen_day] = session


    ### Pass Two: Assigning Rest days
    # We want the non-gym days: grab remaining indexes
    remaining_indexes = [i for i in range(7) if i not in gym_day_indexes]
    # Choose random rest day indexes
    rest_day_indexes = random.sample(remaining_indexes, 2)

    # Ensure Rest days are not next to eachother
    while rest_day_indexes[0] - rest_day_indexes[1] in [1, -1]:
        rest_day_indexes = random.sample(remaining_indexes, 2)

    # Assign rest days as above:
    for index in rest_day_indexes:
        chosen_day = list(week_template)[index]
        week_template[chosen_day] = {"Rest day": []}


    ### Pass Three:
    # Finally we account for the Cardio exercises:

    # Need variable to extract the chosen cardio exercises
    cardio_pass = ["Cardio day"]
    # List of the chosen cardio exercises:
    cardio_sessions = [session for session in exercise_sessions if list(session.keys())[0] in cardio_pass]
    random.shuffle(cardio_sessions)

    # Get the remaining gaps in the schedule:
    final_indexes = [i for i in range(7) if i not in gym_day_indexes and i not in rest_day_indexes]

    # Iterate through the sessions to add accordingly:
    for session in cardio_sessions:
        # Grab out the exercise from the dict for analysis:
        exercise = session['Cardio day'][0]

        # If session is a HIIT, update session to be full plan.
        if exercise.secondary_type == SessionType.HIIT:
            session = generate_HIIT_plan()

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
                chosen_day = list(week_template)[index]
                rest_day_to_update = week_template[chosen_day]
                rest_day_to_update["Rest day"].append(exercise)

            # A HIIT is best done in the gym; therefore if left over we can include within a gym day:
            if exercise.secondary_type == SessionType.HIIT:
                index = random.choice(gym_day_indexes)
                chosen_day = list(week_template)[index]
                week_template[chosen_day].update(session)

        # If no negative criteria are met, add the cardio exercise to the plan
        else: 
            # Get first index:     
            index = final_indexes[0]
            # Get the day of the index:
            chosen_day = list(week_template)[index]
            # Add session to the week plan:
            week_template[chosen_day] = session
            # Remove index to ensure next cardio exercise is added to next free day
            final_indexes.remove(index)

    return week_template


def save_new_plan(exercise_plan: dict, EXERCISE_PLAN_SAVE):
    """Saves plan as JSON"""
    with open(EXERCISE_PLAN_SAVE, 'w') as f:
        data = {}
        for day, session in exercise_plan.items():
            output = {}
            session_type = list(session.keys())[0]
            exercises = list(session.values())[0]

            output[session_type] = [Exercise.to_dict(exercise) for exercise in exercises]

            data[day] = [output]
            
        json.dump(data, f)


###################################~~~MAIN~~~####################################
### CONSTANTS ###

# Initialise weekly plan for filling:
WEEK_TEMPLATE = {
    'Monday': {},
    'Tuesday': {},
    'Wednesday': {},
    'Thursday': {},
    'Friday': {},
    'Saturday': {},
    'Sunday': {}
}

GYM_INDEXES, WEEK_ALLOWANCES, GYM_DAY_CONFIG = get_gym_config() # type: ignore

EXERCISE_PLAN_SAVE = Path(r"src\Data\Exercise\week_workout_plan.json")


def main():
    exercise_sessions = get_exercise_sessions(WEEK_ALLOWANCES)
    last_gym_session = prev_weeks_last_gym_session(EXERCISE_PLAN_SAVE, GYM_DAY_CONFIG)
    exercise_plan = fill_weekly_plan(WEEK_TEMPLATE, GYM_DAY_CONFIG, GYM_INDEXES, last_gym_session, exercise_sessions) #type: ignore
    save_new_plan(exercise_plan, EXERCISE_PLAN_SAVE)
    print('New weekly workout plan generated')



if __name__ == '__main__':
    main()


    # for i, j in zip(exercise_plan, exercise_plan.values()):
    #     print(f'{i}: {list(j.items())}')
