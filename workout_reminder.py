import datetime

from Config.emails import send_email
from Config.config import SMTP_EMAIL
from Data.Exercise.exercises import *

### CONSTANTS ###

week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Week consists of:
WEEK_ALLOWANCES = [
    ExerciseType.BACK_CORE_ARMS,
    ExerciseType.CHEST_SHOULDERS,
    ExerciseType.LEGS,
    ExerciseType.CARDIO,
    ExerciseType.CARDIO,
    ExerciseType.CARDIO,
    ExerciseType.REST,
    ExerciseType.REST
]


### TODO: Update function to account for HIIT and 5K rest day secondary types.

def choose_exercises(day_type: ExerciseType):
    """Returns a set of random exercises depending on the ExerciseType given."""
    if day_type == ExerciseType.BACK_CORE_ARMS:
        exercises = []
        
        #back
        exercises.extend(random.sample([e for e in Exercise.Back_Core_Arm_Day if e.muscle_group == MuscleGroup.UPPER_BACK], 2))
        exercises.extend(random.sample([e for e in Exercise.Back_Core_Arm_Day if e.muscle_group == MuscleGroup.LOWER_BACK], 1))
        #core
        exercises.extend(random.sample([e for e in Exercise.Back_Core_Arm_Day if e.muscle_group == MuscleGroup.CORE], 1))
        #arms
        exercises.extend(random.sample([e for e in Exercise.Back_Core_Arm_Day if e.muscle_group == MuscleGroup.BICEP], 2))
        exercises.extend(random.sample([e for e in Exercise.Back_Core_Arm_Day if e.muscle_group == MuscleGroup.TRICEP], 2))
        
        output = {"Back Core Arm day": exercises}
        return output

    elif day_type == ExerciseType.CHEST_SHOULDERS:
        exercises = []
        
        #chest
        exercises.extend(random.sample([e for e in Exercise.Chest_Shoulder_Day if e.muscle_group == MuscleGroup.CHEST_PRESS], 3))
        exercises.extend(random.sample([e for e in Exercise.Chest_Shoulder_Day if e.muscle_group == MuscleGroup.CHEST_FLY], 1))
        #shoulder
        exercises.extend(random.sample([e for e in Exercise.Chest_Shoulder_Day if e.muscle_group == MuscleGroup.SHOULDER_PRESS], 2))
        exercises.extend(random.sample([e for e in Exercise.Chest_Shoulder_Day if e.muscle_group == MuscleGroup.SHOULDER_SIDE], 2))
        
        return {"Chest Shoulder day": exercises}
    
    elif day_type == ExerciseType.LEGS:
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

    elif day_type == ExerciseType.CARDIO:
        exercises = []
        
        #cardio
        exercises.extend(random.sample(Exercise.Cardio, 3))
        
        return{"Cardio day": exercises}

    elif day_type == ExerciseType.REST: 
        return {"Rest day": []}


# With the exercises chosen we can put that into the week planner to assess where to place each day.

# Function required to take total exercise sessions and return a list of all the sessions:

def get_exercise_sessions(WEEK_ALLOWANCES: list) -> list[dict]:
    """Returns list of exercises to be done in the week."""
    exercise_sessions = []

    for session_type in WEEK_ALLOWANCES:
        if session_type == ExerciseType.REST: pass
        exercise_sessions.append(choose_exercises(session_type))

    return exercise_sessions


# Next we fill the days in the week based on the rules defined



cardio_pass = {ExerciseType.CARDIO: "Cardio day"}


exercise_sessions = get_exercise_sessions(WEEK_ALLOWANCES)

# pass one: assign gym days with gaps.
# pass two: fill gaps with 2 rest days.
# pass three: 2 gaps remaining will have cardio, then assign HIIT to gym day or 5k to gym or rest day.
  
# Choose 3 random weekdays for the gym
# Below are all possible configs of gym days with a day gap between.
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

gym_days_index = random.choice(gym_indexes)

gym_pass = {
    ExerciseType.BACK_CORE_ARMS: "Back Core Arm day",
    ExerciseType.CHEST_SHOULDERS: "Chest Shoulder day",
    ExerciseType.LEGS: "Leg day",
}

gym_sessions = [session for session in exercise_sessions if list(session.keys())[0] in gym_pass.values()]

random.shuffle(gym_sessions)

exercise_plan = {}

# pass one
for index, session in zip(gym_days_index, gym_sessions):
    chosen_day = week_days[index]
    exercise_plan[chosen_day] = session

remaining_indexes = [i for i in range(7) if i not in gym_days_index]

# pass two
rest_day_indexes = random.sample(remaining_indexes, 2)

for index in rest_day_indexes:
    chosen_day = week_days[index]
    exercise_plan[chosen_day] = {"Rest day": []}


# pass three
final_indexes = [i for i in range(7) if i not in gym_days_index and i not in rest_day_indexes]
cardio_sessions = [session for session in exercise_sessions if list(session.keys())[0] in cardio_pass.values()]
random.shuffle(cardio_sessions)

"""
We have three cardio exercises.

Want to fill remaining indexes first.

Any overspill we want to have shared on another day (HIIT on Gym day, or 5K on Rest day)

Ideally want to maintain shuffle to keep variety intact.

Problems can occur if shuffled and it assigns the secondary types first.
The only way around this is to not shuffle.
We would then have to ensure any non-secondaryTyped cardio exercises are initialised first.

The more non-secondary typed cardio exercises that are added, the more likely that there are 3 chosen and therefore the algorythm would break.
"""

# We can possibly get around this issue by assigning cardio before the rest days.
# If 6 days are applied then HIIT would never be in a gym day - leaving a redundant secondary type



for session in cardio_sessions:
    exercise = session['Cardio day'][0]
        
    if not exercise.secondary_type:
        index = final_indexes[0]
        chosen_day = week_days[index]
        exercise_plan[chosen_day] = session
        final_indexes.remove(index)

    if exercise.secondary_type == ExerciseType.REST:
        ...

    if exercise.secondary_type == ExerciseType.HIIT:
        # Generate hiit workout
        # Add to gym day
        ...





#BUG currently weekdays out of order

#Print check
for j, i in zip(exercise_plan.keys(), exercise_plan.values()):
    print(f'{j}: {list(i.keys())}')


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
