import datetime
from Config.emails import send_email


# Updates:
# Create a flexible plan including gym workouts
# Add input space for weights lifted to keep track and update plan accordingly
# 

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
send_email(subject, msg)