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

### Functions ###

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
        
        return {"Back Core Arm day": exercises}

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

    elif day_type == ExerciseType.REST: # Currently Unused
        return {"Rest day": []}


def get_exercise_sessions(WEEK_ALLOWANCES: list) -> list[dict]:
    """Returns list of exercises to be done in the week."""
    exercise_sessions = []

    for session_type in WEEK_ALLOWANCES:
        if session_type == ExerciseType.REST: pass
        exercise_sessions.append(choose_exercises(session_type))

    return exercise_sessions

exercise_sessions = get_exercise_sessions(WEEK_ALLOWANCES)

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

gym_day_indexes = random.choice(gym_indexes)

gym_pass = {
    ExerciseType.BACK_CORE_ARMS: "Back Core Arm day",
    ExerciseType.CHEST_SHOULDERS: "Chest Shoulder day",
    ExerciseType.LEGS: "Leg day",
}

gym_sessions = [session for session in exercise_sessions if list(session.keys())[0] in gym_pass.values()]

random.shuffle(gym_sessions)

exercise_plan = {
    'Monday': {},
    'Tuesday': {},
    'Wednesday': {},
    'Thursday': {},
    'Friday': {},
    'Saturday': {},
    'Sunday': {}
}

# pass one
for index, session in zip(gym_day_indexes, gym_sessions):
    chosen_day = week_days[index]
    exercise_plan[chosen_day] = session

remaining_indexes = [i for i in range(7) if i not in gym_day_indexes]

# pass two
rest_day_indexes = random.sample(remaining_indexes, 2)

for index in rest_day_indexes:
    chosen_day = week_days[index]
    exercise_plan[chosen_day] = {"Rest day": []}

# pass three
cardio_pass = {ExerciseType.CARDIO: "Cardio day"}
final_indexes = [i for i in range(7) if i not in gym_day_indexes and i not in rest_day_indexes]
cardio_sessions = [session for session in exercise_sessions if list(session.keys())[0] in cardio_pass.values()]
random.shuffle(cardio_sessions)

for session in cardio_sessions:
    exercise = session['Cardio day'][0]

    # If session is a HIIT, update session to be full plan.
    if exercise.secondary_type == ExerciseType.HIIT:
        session = HIIT._get_plan()

    if not final_indexes:
        if not exercise.secondary_type:
            # Sometimes we get lucky and have less cardio in a week.

            # This could be updated in future to swap in to a previous cardio day if it has a secondary_type.
            # Or if not to just have one less Rest day.
            # But let's start easy for now.  
            pass

        if exercise.secondary_type == ExerciseType.REST:
            # Current rest indexes are as above- choose one at random and add the 5k.
            index = random.choice(rest_day_indexes)
            chosen_day = week_days[index]
            rest_day_to_update = exercise_plan[chosen_day]
            # Hopefully below adds the 5K to the rest day dict values.
            rest_day_to_update["Rest day"].append(exercise) #TODO check if correclty happens


        if exercise.secondary_type == ExerciseType.HIIT: #TODO check if correclty happens
            index = random.choice(gym_day_indexes)
            chosen_day = week_days[index]
            exercise_plan[chosen_day] = session
    
    else:      
        index = final_indexes[0]
        chosen_day = week_days[index]
        exercise_plan[chosen_day] = session
        final_indexes.remove(index)


#Print check
for j, i in zip(exercise_plan.keys(), exercise_plan.values()):
    print(f'{j}: {list(i.keys())}')



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

#Send reminder
#send_email(subject, msg, SMTP_EMAIL)
