import random

from dataclasses import dataclass, field

from .exercise import Exercise
from .session_type import SessionType
from .muscle_group import MuscleGroup


@dataclass
class WorkoutSession:
    name: str
    exercises: list[Exercise] = field(default_factory=list)
    exercise_type: SessionType = field(default=None) #type: ignore
    muscle_groups: list[MuscleGroup] = field(default=None) #type: ignore

    ### Init methods ###
    @staticmethod
    def init_all_exercises(list_of_exercises: list[Exercise]):
        return WorkoutSession("All Exercises", exercises=list_of_exercises)

    @staticmethod
    def get_exercises_by_type(all_exercises, exercise_type: SessionType) -> list[Exercise]:
        return [exercise for exercise in all_exercises.exercises if exercise.type == exercise_type]

    @staticmethod
    def init_workout_by_type(all_exercises, exercise_type: SessionType):
        name=exercise_type.value
        exercises = WorkoutSession.get_exercises_by_type(all_exercises, exercise_type)
        return WorkoutSession(name, exercises=exercises, exercise_type=exercise_type)

    ### Workout Generation Methods ###
    @staticmethod
    def grab_selection(exercise_list: list[Exercise], muscle_group: MuscleGroup, number: int) -> list[Exercise]:
        return random.sample([e for e in exercise_list if e.muscle_group == muscle_group], number)


    ### Helper methods ###
    def add_exercise(self, exercise: Exercise):
        self.exercises.append(exercise)

    def add_exercises(self, list_of_exercises: list[Exercise]):
        self.exercises.extend(list_of_exercises)

    def remove_exercise(self, exercise: Exercise):
        self.exercises.remove(exercise)


    ### Unfinished/Unused methods ###
    @staticmethod
    def to_string(session: "WorkoutSession") -> str:
        ...
        
    @staticmethod
    def move_exercise(exercise: Exercise, from_workout_type, to_workout_type): 
        """Function for moving an exercise between workouts"""
        # Ideally this could be utilised within the front end; once the database is in use.
        # This may not be needed as the schema can just be updated backend in the construction of the backed datatypes
        pass



### Init db seeding Exercises ###
ALL_EXERCISES = WorkoutSession.init_all_exercises([
    #Back:
    Exercise("Deadlifts", SessionType.BACK_CORE_ARMS, MuscleGroup.LOWER_BACK, weight=100, reps=5),
    Exercise("Romanian deadlifts", SessionType.BACK_CORE_ARMS, MuscleGroup.LOWER_BACK, weight=30, reps=10),
    Exercise("Bent over rows", SessionType.BACK_CORE_ARMS, MuscleGroup.UPPER_BACK, weight=40, reps=10),
    Exercise("Isolated rows", SessionType.BACK_CORE_ARMS, MuscleGroup.UPPER_BACK, weight=24, reps=8),
    Exercise("Reverse fly", SessionType.BACK_CORE_ARMS, MuscleGroup.UPPER_BACK, weight=25, reps=10),
    Exercise("Lat pull downs", SessionType.BACK_CORE_ARMS, MuscleGroup.UPPER_BACK, weight=50, reps=10),
    
    #Core:
    Exercise("Crunches", SessionType.BACK_CORE_ARMS, MuscleGroup.CORE, reps=20),
    Exercise("Weighted Situps", SessionType.BACK_CORE_ARMS, MuscleGroup.CORE, weight=10, reps=12),
    
    #Arms:
    Exercise("Face-pulls", SessionType.BACK_CORE_ARMS, MuscleGroup.BICEP, weight=38, reps=10),
    Exercise("Bicep curls", SessionType.BACK_CORE_ARMS, MuscleGroup.BICEP, weight=8, reps=10),
    Exercise("Barbell bicep curls", SessionType.BACK_CORE_ARMS, MuscleGroup.BICEP, weight=25, reps=10),
    Exercise("Pull ups", SessionType.BACK_CORE_ARMS, MuscleGroup.BICEP, reps=10),
    Exercise("Skull crushers", SessionType.BACK_CORE_ARMS, MuscleGroup.TRICEP, weight=10, reps=10),
    Exercise("Dips", SessionType.BACK_CORE_ARMS, MuscleGroup.TRICEP, reps=10),
    Exercise("Tricep pull downs", SessionType.BACK_CORE_ARMS, MuscleGroup.TRICEP, weight=40, reps=10),
    Exercise("Tricep Shoulder Lifts", SessionType.BACK_CORE_ARMS, MuscleGroup.TRICEP, weight=20, reps=10),
    
    #Chest:
    Exercise("Bench press", SessionType.CHEST_SHOULDERS, MuscleGroup.CHEST_PRESS, weight=50, reps=10),
    Exercise("Press ups", SessionType.CHEST_SHOULDERS, MuscleGroup.CHEST_PRESS, reps=15),
    Exercise("Incline press", SessionType.CHEST_SHOULDERS, MuscleGroup.CHEST_PRESS, weight=40, reps=10),
    Exercise("Decline press", SessionType.CHEST_SHOULDERS, MuscleGroup.CHEST_PRESS, weight=40, reps=10),
    Exercise("Seated press", SessionType.CHEST_SHOULDERS, MuscleGroup.CHEST_PRESS, weight=40, reps=10),
    Exercise("Freeweight Fly", SessionType.CHEST_SHOULDERS, MuscleGroup.CHEST_FLY, weight=14, reps=10),
    Exercise("Cable fly", SessionType.CHEST_SHOULDERS, MuscleGroup.CHEST_FLY, weight=50, reps=10),
    
    #Shoulders:
    Exercise("Side shoulder lifts", SessionType.CHEST_SHOULDERS, MuscleGroup.SHOULDER_SIDE, weight=6, reps=10),
    Exercise("Front shoulder lifts", SessionType.CHEST_SHOULDERS, MuscleGroup.SHOULDER_SIDE, weight=10, reps=10),
    Exercise("Standing Shoulder press", SessionType.CHEST_SHOULDERS, MuscleGroup.SHOULDER_PRESS, weight=30, reps=8),
    Exercise("Seated Shoulder press", SessionType.CHEST_SHOULDERS, MuscleGroup.SHOULDER_PRESS, weight=25, reps=8),
    
    #Legs:
    Exercise("Squats", SessionType.LEGS, MuscleGroup.WHOLE_LEG, weight=80, reps=8),
    Exercise("Wall sits", SessionType.LEGS, MuscleGroup.WHOLE_LEG, time=30),
    Exercise("Leg Curls", SessionType.LEGS, MuscleGroup.HAMSTRINGS, weight=45, reps=10),
    Exercise("Leg extensions", SessionType.LEGS, MuscleGroup.QUADS, weight=55, reps=10),
    Exercise("Leg press", SessionType.LEGS, MuscleGroup.WHOLE_LEG, weight=120, reps=10),
    Exercise("Lunges", SessionType.LEGS, MuscleGroup.GLUTES, weight=10, reps=12),
    Exercise("Hungarian split squats", SessionType.LEGS, MuscleGroup.GLUTES, weight=10, reps=10),
    
    #HIIT:
    Exercise("Mountain climbers", SessionType.HIIT, MuscleGroup.CORE, time=30),
    Exercise("Plank", SessionType.HIIT, MuscleGroup.CORE, time=60),
    Exercise("Press-ups", SessionType.HIIT, MuscleGroup.CHEST_PRESS, time=30),
    Exercise("Sit-ups", SessionType.HIIT, MuscleGroup.CORE, time=30),
    Exercise("Box-jump", SessionType.HIIT, MuscleGroup.WHOLE_LEG, time=30),
    Exercise("Paratroopers", SessionType.HIIT, MuscleGroup.UPPER_BACK, time=30),
    Exercise("Side plank", SessionType.HIIT, MuscleGroup.CORE, time=30),
    Exercise("Raised plank", SessionType.HIIT, MuscleGroup.CORE, time=60),
    Exercise("Shoulder taps", SessionType.HIIT, MuscleGroup.CORE, time=45),
    Exercise("Reverse crunches", SessionType.HIIT, MuscleGroup.CORE, time=30),
    Exercise("Bicycle Crunches", SessionType.HIIT, MuscleGroup.CORE, time=30),
    Exercise("V-sits", SessionType.HIIT, MuscleGroup.CORE, time=30),
    Exercise("Leg raises", SessionType.HIIT, MuscleGroup.CORE, time=30),
    Exercise("Static shoulder lifts", SessionType.HIIT, MuscleGroup.SHOULDER_SIDE, weight=4, time=30),
    Exercise("Mobile shoulder lifts", SessionType.HIIT, MuscleGroup.SHOULDER_SIDE, weight=6, time=30),
    Exercise("Bicep curls", SessionType.HIIT, MuscleGroup.BICEP, weight=8, time=30),
    Exercise("Tricep lifts", SessionType.HIIT, MuscleGroup.TRICEP, weight=16, time=30),
    Exercise("Squats", SessionType.HIIT, MuscleGroup.WHOLE_LEG, weight=40, time=30),
    Exercise("Jumping Lunges", SessionType.HIIT, MuscleGroup.QUADS, time=30),
    Exercise("Lunges", SessionType.HIIT, MuscleGroup.QUADS, weight=20, time=30),
    Exercise("Romanian deadlifts", SessionType.HIIT, MuscleGroup.LOWER_BACK, weight=20, time=30),
    Exercise("Russian twists", SessionType.HIIT, MuscleGroup.CORE, weight=10, time=30),
    Exercise("Burpees", SessionType.HIIT, MuscleGroup.WHOLE_LEG, time=45),
    Exercise("Single-leg squats", SessionType.HIIT, MuscleGroup.GLUTES, time=30),
    Exercise("Close-grip push-ups", SessionType.HIIT, MuscleGroup.CHEST_PRESS, time=30),
    Exercise("Glute bridges", SessionType.HIIT, MuscleGroup.GLUTES, weight=30, time=30),
    Exercise("Incline push-ups", SessionType.HIIT, MuscleGroup.CHEST_PRESS, weight=20, time=30),
    Exercise("Jumping jacks", SessionType.HIIT, MuscleGroup.SHOULDER_SIDE, weight=6, time=30),
    Exercise("Plank jacks", SessionType.HIIT, MuscleGroup.CORE, time=30),
    Exercise("Jump squats", SessionType.HIIT, MuscleGroup.QUADS, time=30),
    Exercise("Superman plank", SessionType.HIIT, MuscleGroup.CORE, time=30),
    
    #Cardio:
    Exercise("FARTLEK 10k", SessionType.CARDIO),
    Exercise("10K", SessionType.CARDIO),
    Exercise("5K", SessionType.CARDIO, secondary_type=SessionType.REST),
    Exercise("HIIT workout", SessionType.CARDIO, secondary_type=SessionType.HIIT),
    Exercise("FARTLEK 5k", SessionType.CARDIO, secondary_type=SessionType.REST),
    #half_maraton = Exercise("Half marathon", SessionType.CARDIO)

    #Rest:
    Exercise("Rest Day", SessionType.REST)
])


### init workout lists by SessionType ###
BACK_CORE_ARM_EXERCISES = WorkoutSession.get_exercises_by_type(ALL_EXERCISES, SessionType.BACK_CORE_ARMS)
CHEST_SHOULDER_EXERCISES = WorkoutSession.get_exercises_by_type(ALL_EXERCISES, SessionType.CHEST_SHOULDERS)
LEG_EXERCISES = WorkoutSession.get_exercises_by_type(ALL_EXERCISES, SessionType.LEGS)
CARDIO_EXERCISES = WorkoutSession.get_exercises_by_type(ALL_EXERCISES, SessionType.CARDIO)
HIIT_EXERCISES = WorkoutSession.get_exercises_by_type(ALL_EXERCISES, SessionType.HIIT)


### randomised Generation function function ###
def get_exercise_session_by_type(day_type: SessionType) -> dict: #type: ignore
    """Returns a set of random exercises depending on the SessionType given."""
    if day_type == SessionType.BACK_CORE_ARMS:
        exercises = []
        
        #back
        exercises.extend(WorkoutSession.grab_selection(BACK_CORE_ARM_EXERCISES, MuscleGroup.UPPER_BACK, 2))
        exercises.extend(WorkoutSession.grab_selection(BACK_CORE_ARM_EXERCISES, MuscleGroup.LOWER_BACK, 1))
        #core
        exercises.extend(WorkoutSession.grab_selection(BACK_CORE_ARM_EXERCISES, MuscleGroup.CORE, 1))
        #arms
        exercises.extend(WorkoutSession.grab_selection(BACK_CORE_ARM_EXERCISES, MuscleGroup.BICEP, 2))
        exercises.extend(WorkoutSession.grab_selection(BACK_CORE_ARM_EXERCISES, MuscleGroup.TRICEP, 2))
        
        return {day_type.value: exercises}

    elif day_type == SessionType.CHEST_SHOULDERS:
        exercises = []
        
        #chest
        exercises.extend(WorkoutSession.grab_selection(CHEST_SHOULDER_EXERCISES, MuscleGroup.CHEST_PRESS, 3))
        exercises.extend(WorkoutSession.grab_selection(CHEST_SHOULDER_EXERCISES, MuscleGroup.CHEST_FLY, 1))
        #shoulder
        exercises.extend(WorkoutSession.grab_selection(CHEST_SHOULDER_EXERCISES, MuscleGroup.SHOULDER_PRESS, 2))
        exercises.extend(WorkoutSession.grab_selection(CHEST_SHOULDER_EXERCISES, MuscleGroup.SHOULDER_SIDE, 2))
        
        return {day_type.value: exercises}
    
    elif day_type == SessionType.LEGS:
        exercises = []

        #whole leg
        exercises.extend(WorkoutSession.grab_selection(LEG_EXERCISES, MuscleGroup.WHOLE_LEG, 3))
        #quads
        exercises.extend(WorkoutSession.grab_selection(LEG_EXERCISES, MuscleGroup.QUADS, 1))
        #hammys
        exercises.extend(WorkoutSession.grab_selection(LEG_EXERCISES, MuscleGroup.HAMSTRINGS, 1))
        #glutes
        exercises.extend(WorkoutSession.grab_selection(LEG_EXERCISES, MuscleGroup.GLUTES, 1))

        return {day_type.value: exercises}

    elif day_type == SessionType.CARDIO:
        exercises = []
        
        #cardio
        exercises.extend(random.sample(CARDIO_EXERCISES, 1))
        
        return{day_type.value: exercises}
