import schedule
import time
import subprocess

### Constants ###
# Set the time for the reminder to be sent (in 24-hour format)
WORKOUT_GENERATION_TIME = "00:01"
WORKOUT_REMINDER_TIME = "09:59"
MEALPLAN_TIME = "09:00"

### TODO Helper functions could be implemented to change the scheduled time.


### Scheduled functions ###
def create_workout_plan():
    subprocess.call(['python', 'exercise_plan_generator.py'])
    print('New weekly exercise plan generated.')

def send_workout_reminder():
    subprocess.call(['python', "workout_reminder.py"])
    print('workout reminder sent')

def create_meal_plan():
    subprocess.call(['python', 'shopping_list_generator.py'])
    print("week's meal plan created")


### Main() ###
def scheduler():
    # Schedule the reminder to be sent at the specified time each day
    schedule.every().day.at(WORKOUT_REMINDER_TIME).do(send_workout_reminder)
    schedule.every().monday.at(WORKOUT_GENERATION_TIME).do(create_workout_plan)
    schedule.every().sunday.at(MEALPLAN_TIME).do(create_meal_plan)

    print('Starting Scheduler')
    # Loop to check for scheduled tasks
    try:
        print('Scheduler running...')
        while True:
            schedule.run_pending()
            time.sleep(30)  # check for new tasks every half-minute
    except Exception as e:
        print(f'Scheduler interrupted: {e}')


if __name__ == "__main__":
    scheduler()