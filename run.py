import schedule
import time
import subprocess

# Set the time for the reminder to be sent (in 24-hour format)
SEND_TIME = "10:59"

# Function to send the reminder
def send_reminder():
    subprocess.call(['python', "workout_reminder.py"])
    print('workout reminder sent')

def create_meal_plan():
    subprocess.call(['python', 'shopping_list.py'])
    print("week's meal plan created")

# Schedule the reminder to be sent at the specified time each day
schedule.every().day.at(SEND_TIME).do(send_reminder)
schedule.every().monday.at('16:00').do(create_meal_plan)

print('Starting Scheduler')
# Loop to check for scheduled tasks
try:
    print('Scheduler running...')
    while True:
        schedule.run_pending()
        time.sleep(60) # check for new tasks every minute
except Exception as e:
    print(f'Scheduler interrupted: {e}')