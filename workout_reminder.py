import datetime

from Config.emails import send_email
from Config.config import SMTP_EMAIL
from Data.Exercise.exercises import *

### CONSTANTS ###

week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Week consists of:
WEEK_ALLOWANCES = {
    ExerciseType.BACK_CORE_ARMS: 1,
    ExerciseType.CHEST_SHOULDERS: 1,
    ExerciseType.LEGS: 1,
    ExerciseType.CARDIO: 3,
    ExerciseType.REST: 2
}


### TODO: Update function to account for HIIT and 5K rest day secondary types.


def choose_exercises(day_type: ExerciseType) -> dict:
    """Returns a set of random exercises depending on the ExerciseType given."""
    if day_type == ExerciseType.BACK_CORE_ARMS:
        exercises = []
        
        #back
        exercises.extend(random.sample([e for e in Exercise.Back_Core_Arm_Day if Exercise.muscle_group == MuscleGroup.UPPER_BACK], 2))
        exercises.extend(random.sample([e for e in Exercise.Back_Core_Arm_Day if Exercise.muscle_group == MuscleGroup.LOWER_BACK], 1))
        #core
        exercises.extend(random.sample([e for e in Exercise.Back_Core_Arm_Day if Exercise.muscle_group == MuscleGroup.CORE], 1))
        #arms
        exercises.extend(random.sample([e for e in Exercise.Back_Core_Arm_Day if Exercise.muscle_group == MuscleGroup.BICEP], 2))
        exercises.extend(random.sample([e for e in Exercise.Back_Core_Arm_Day if Exercise.muscle_group == MuscleGroup.TRICEP], 2))
        
        return {"Back Core Arm day": exercises}

    elif day_type == ExerciseType.CHEST_SHOULDERS:
        exercises = []
        
        #chest
        exercises.extend(random.sample([e for e in Exercise.Chest_Shoulder_Day if Exercise.muscle_group == MuscleGroup.CHEST_PRESS], 3))
        exercises.extend(random.sample([e for e in Exercise.Chest_Shoulder_Day if Exercise.muscle_group == MuscleGroup.CHEST_FLY], 1))
        #shoulder
        exercises.extend(random.sample([e for e in Exercise.Chest_Shoulder_Day if Exercise.muscle_group == MuscleGroup.SHOULDER_PRESS], 2))
        exercises.extend(random.sample([e for e in Exercise.Chest_Shoulder_Day if Exercise.muscle_group == MuscleGroup.SHOULDER_SIDE], 2))
        
        return {"Chest Shoulder day": exercises}
    
    elif day_type == ExerciseType.LEGS:
        exercises = []

        #whole leg
        exercises.extend(random.sample([e for e in Exercise.Leg_Day if Exercise.muscle_group == MuscleGroup.WHOLE_LEG], 3))
        #quads
        exercises.extend(random.sample([e for e in Exercise.Leg_Day if Exercise.muscle_group == MuscleGroup.QUADS], 1))
        #hammys
        exercises.extend(random.sample([e for e in Exercise.Leg_Day if Exercise.muscle_group == MuscleGroup.HAMSSTRINGS], 1))
        #glutes
        exercises.extend(random.sample([e for e in Exercise.Leg_Day if Exercise.muscle_group == MuscleGroup.GLUTES], 1))

        return {"Leg day": exercises}

    elif day_type == ExerciseType.CARDIO:
        exercises = []
        
        #cardio
        exercises.extend(random.sample(Exercise.Cardio, 3))
        
        return{"Cardio day": exercises}

    elif day_type == ExerciseType.REST: 
        return {"Rest day": None}


# With the exercises chosen we can put that into the week planner to assess where to place each day.

# Function required to take total exercise sessions and return a list of all the sessions:

def get_exercise_sessions(WEEK_ALLOWANCES: dict) -> list[dict]:
    """Returns list of exercises to be done in the week."""
    exercise_sessions = []

    for session_type in WEEK_ALLOWANCES.keys():
        if session_type == ExerciseType.REST: pass
        exercise_sessions.extend(choose_exercises(session_type))

    return exercise_sessions


# Next we fill the days in the week based on the rules defined

pass_one = {
    ExerciseType.BACK_CORE_ARMS: "Back Core Arm day",
    ExerciseType.CHEST_SHOULDERS: "Chest Shoulder day",
    ExerciseType.LEGS: "Leg day",
}

pass_two = {ExerciseType.REST: "Rest day"} # Need iterable so do this another way

pass_three = {ExerciseType.CARDIO: "Cardio day"}


exercise_plan = {}
exercise_sessions = get_exercise_sessions(WEEK_ALLOWANCES)

# pass one: assign gym days with gaps.
# pass two: fill gaps with 2 rest days.
# pass three: 2 gaps remaining will have cardio, then assign HIIT to gym day or 5k to gym or rest day.

# Pass one
   
# Choose 3 random weekdays for the gym
gym_days = random.sample(week_days, 3)

# Create the week plan

prev_day = None
for day in week_days:
  if day in gym_days and prev_day != "Gym":
    # Add the gym day to the week plan
    exercise_plan[day] = "Gym"
  else:
    # Add a gap to the week plan
    exercise_plan[day] = "Gap"
  prev_day = exercise_plan[day]

    


# fill days after

##################################################################################
# Set up bodyweight exercise plan
plan = {
    'Monday': 'Squats, Lunges, Push-ups, Plank, Sit-ups',
    'Tuesday': 'Dips, Inverted rows, Russian twists, Mountain climbers, Side plank',
    'Wednesday': 'Rest day',
    'Thursday': 'Burpees, Single-leg squats, Close-grip push-ups, Bicycle crunches, Glute bridges',
    'Friday': 'Incline push-ups, Jumping jacks, Plank jacks, Jump squats, V-ups',
    'Saturday': 'Rest day',
    'Sunday': 'Jumping lunges, Tricep dips, Box jumps, Superman plank, Bicycle crunches'
}

# Get current day of the week
day = datetime.datetime.today().strftime('%A')

# Build email info
msg = ("Today's bodyweight exercises: " + plan[day])
subject = "Bodyweight Exercise Reminder"

# Send reminder
#send_email(subject, msg, SMTP_EMAIL)
