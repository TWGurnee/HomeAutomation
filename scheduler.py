#!/usr/bin/env python -u

import sys
import schedule
import time
import subprocess
import threading


### Constants ###
# Set the time for the reminder to be sent (in 24-hour format)
WORKOUT_GENERATION_TIME = "00:01"
WORKOUT_REMINDER_TIME = "09:00"
MEALPLAN_TIME = "09:00"

### TODO Helper functions could be implemented to change the scheduled time.
# - can update the scheduler to a class with cls methods to change the time.
# - can then ensure that the run method starts the scheduler in main().


### Scheduled functions ###
def create_workout_plan():
    subprocess.call(['python', 'exercise_plan_generator.py'])

def send_workout_reminder():
    subprocess.call(['python', "workout_reminder.py"])

def create_meal_plan():
    subprocess.call(['python', 'shopping_list_generator.py'])


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
            time.sleep(30) # check for new tasks every half-minute

    except Exception as e:
        print(f'Scheduler interrupted: {e}')


class Scheduler():

    def __init__(self):
        self.WORKOUT_GENERATION_TIME = "00:01"
        self.WORKOUT_REMINDER_TIME = "09:00"
        self.MEALPLAN_TIME = "09:00"


    def change_scheduled_time(self, option: str, new_time: str):
        if option == "workout-generation":
            self.WORKOUT_GENERATION_TIME = new_time

        if option == "workout-reminder":
            self.WORKOUT_REMINDER_TIME = new_time

        if option == "mealplan-generation":
            self.MEALPLAN_TIME = new_time


    def scheduler(self):
        # Schedule the reminder to be sent at the specified time each day
        schedule.every().day.at(self.WORKOUT_REMINDER_TIME).do(send_workout_reminder)
        schedule.every().monday.at(self.WORKOUT_GENERATION_TIME).do(create_workout_plan)
        schedule.every().sunday.at(self.MEALPLAN_TIME).do(create_meal_plan)

        print('Starting Scheduler')
        # Loop to check for scheduled tasks
        try:
            print('Scheduler running...')
            while True:
                schedule.run_pending()
                time.sleep(1) # check for new tasks every half-minute

        except Exception as e:
            print(f'Scheduler interrupted: {e}')


    def run(self):
        scheduling_thread = threading.Thread(target=self.scheduler, daemon=True)
        scheduling_thread.start()
   


if __name__ == "__main__":
    scheduling_thread = threading.Thread(target=scheduler, daemon=True)
    scheduling_thread.run()
