from pathlib import Path

import datetime

from Config.emails import send_email
from Config.config import SMTP_EMAIL
from exercise_plan_generator import load_current_plan
from Data.Exercise.exercises import *

# Set up bodyweight exercise plan ##TODO Import from saved locations
plan = {
    'Monday': 'Squats, Lunges, Push-ups, Plank, Sit-ups',
    'Tuesday': 'Dips, Inverted rows, Russian twists, Mountain climbers, Side plank',
    'Wednesday': 'Rest day',
    'Thursday': 'Burpees, Single-leg squats, Close-grip push-ups, Bicycle crunches, Glute bridges',
    'Friday': 'Incline push-ups, Jumping jacks, Plank jacks, Jump squats, V-ups',
    'Saturday': 'Rest day',
    'Sunday': 'Jumping lunges, Tricep dips, Box jumps, Superman plank, Bicycle crunches'
}

# to update plan we want to import the dict from the path

# we then grab the day but convert the response accordingly.

# Currently the Exercise class can be converted to a string, but not all days will have an exercise.


SAVE_LOCATION = Path.cwd() / r"Data\Exercise\workouts.json"

plan = load_current_plan(SAVE_LOCATION) # TODO: update loading function so Exercise Objexts are made.

# Get current day of the week
day = datetime.datetime.today().strftime('%A')

current_days_session = plan[day]
current_days_session = current_days_session[0]

day_type = list(current_days_session.keys())[0]

exercises = list(current_days_session.values())[0]
print(exercises)

# Build email info
msg = ("Today's exercise session: " + day_type)
if exercises:
    msg+=[Exercise.to_str(exercise) for exercise in exercises]

print(msg)

subject = "Exercise Reminder"

# Send reminder
# send_email(subject, msg, SMTP_EMAIL)
