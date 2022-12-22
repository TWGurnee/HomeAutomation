import schedule
import time
import subprocess

# Set the time for the reminder to be sent (in 24-hour format)
WORKOUT_TIME = "10:59"
MEALPLAN_TIME = "16:00"

# Function to send the reminder
def send_workout_reminder():
    subprocess.call(['python', "workout_reminder.py"])
    print('workout reminder sent')

def create_meal_plan():
    subprocess.call(['python', 'shopping_list.py'])
    print("week's meal plan created")

# Schedule the reminder to be sent at the specified time each day
schedule.every().day.at(WORKOUT_TIME).do(send_workout_reminder)
schedule.every().monday.at(MEALPLAN_TIME).do(create_meal_plan)

print('Starting Scheduler')
# Loop to check for scheduled tasks
try:
    print('Scheduler running...')
    while True:
        schedule.run_pending()
        time.sleep(30) # check for new tasks every half-minute
except Exception as e:
    print(f'Scheduler interrupted: {e}')