from pathlib import Path

import datetime

from .Config.emails import send_email
from .Config.config import SMTP_EMAIL

from .Data.helpers import load_current_plan
from .Data.Exercise import Exercise

### Constants ###

EXERCISE_PLAN_SAVE = Path(r"Data\Exercise\week_workout_plan.json")

### Main() ###

def todays_workout_to_string(EXERCISE_PLAN_SAVE):
    plan = load_current_plan(EXERCISE_PLAN_SAVE) # TODO: update loading function so Exercise Objexts are made.

    day = datetime.datetime.today().strftime('%A')

    # Get current days session from the saved plan
    current_days_session = plan[day]
    current_days_session = current_days_session[0]

    # Extract session info from session.
    # Session is dict format: {session : [Exercise.to_dict]}
    day_type = list(current_days_session.keys())[0]
    exercises = list(current_days_session.values())[0]

    # Build email info
    msg = ("Today's exercise session: " + day_type)
    if exercises:
        exercises_string = '\n'.join([Exercise.from_dict_to_str(exercise) for exercise in exercises])
        msg += exercises_string

    print(msg)

    return msg


def main():
    subject = "Exercise Reminder"
    msg = todays_workout_to_string(EXERCISE_PLAN_SAVE)
    send_email(subject, msg, SMTP_EMAIL)

# Run
if __name__ == '__main__':
    main()