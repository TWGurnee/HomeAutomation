from dataclasses import dataclass, field, asdict, replace
from enum import Enum
from copy import deepcopy
import random
import json


class SessionType(Enum):
    BACK_CORE_ARMS = 1
    CHEST_SHOULDERS = 2
    LEGS = 3
    CARDIO = 4
    HIIT = 5
    REST = 6


class MuscleGroup(Enum):
    # BACK_CORE_ARMS
    LOWER_BACK = 1
    UPPER_BACK = 2
    CORE = 3
    BICEP = 4
    TRICEP = 5
    #CHESTSHOULDERS
    CHEST_PRESS = 6
    CHEST_FLY = 7
    SHOULDER_PRESS = 8
    SHOULDER_SIDE = 9
    #LEGS
    QUADS = 10
    HAMSSTRINGS = 11
    GLUTES = 12
    WHOLE_LEG = 13


@dataclass
class Exercise:
    name: str
    type: SessionType
    muscle_group: MuscleGroup = field(default=None, metadata={"description": "The group of muscles used in the exercise. Required to ensure a balanced workout"})
    weight: int = field(default=None, metadata={"description": "Weight in Kg used for the exercise"})
    reps: int = field(default=None, metadata={"description": "Number of reps to perform for the exercise"})
    time: int = field(default=None, metadata={"description": "Field for the best time, target time, or input time. Measured in seconds"})
    secondary_type: SessionType = field(default=None, metadata={"description": "The secondary type of an exercise. Current use cases are HIIT and 5K to allow for appropriate plan generation"})
    #sets: int = field(default_factory=lambda: 4)

    Back_Core_Arm_Day = []
    Chest_Shoulder_Day = []
    Leg_Day = []
    Cardio = []
    HIIT = []
    Rest = []

    @staticmethod 
    def init_lists(): # supposedly required to ensure only one copy of each list is stored in memory.
        Exercise.Back_Core_Arm_Day = []
        Exercise.Chest_Shoulder_Day = []
        Exercise.Leg_Day = []
        Exercise.Cardio = []
        Exercise.HIIT = []
        Exercise.Rest = []

    def __post_init__(self):
        if not Exercise.Back_Core_Arm_Day:
            Exercise.init_lists() #### Not sure if required or if has to be a class method.
        if self.type == SessionType.BACK_CORE_ARMS:
            self.Back_Core_Arm_Day.append(self)
        elif self.type == SessionType.CHEST_SHOULDERS:
            self.Chest_Shoulder_Day.append(self)
        elif self.type == SessionType.LEGS:
            self.Leg_Day.append(self)
        elif self.type == SessionType.CARDIO:
            self.Cardio.append(self)
        elif self.type == SessionType.HIIT:
            self.HIIT.append(self)
        elif self.type == SessionType.REST:
            self.Rest.append(self)

    @staticmethod
    def custom_asdict_factory(data):

        def convert_value(obj):
            if isinstance(obj, Enum):
                return obj.value
            return obj

        return dict((k, convert_value(v)) for k, v in data)

    @staticmethod
    def to_dict(exercise: "Exercise") -> dict:
        return asdict(exercise, dict_factory=Exercise.custom_asdict_factory)

    @staticmethod
    def from_dict(data: dict) -> "Exercise":
        return replace(Exercise, **data) #type: ignore

    @staticmethod
    def to_json(exercise: "Exercise") -> str:
        data = asdict(exercise)
        return json.dumps(data)

    @staticmethod
    def to_str(exercise: "Exercise") -> str:
        output = ""
        output += f'\n- {exercise.name}\n'
        if exercise.weight: output += f'{exercise.weight}kg,'
        if exercise.reps: output += f'for {exercise.reps} reps.'
        if exercise.time: output += f'for {exercise.time} seconds'
        return output
        # Filtering function required for removing unrequired info in instructions.
        # 

        # e = Exercise.to_dict(exercise)


@dataclass
class WorkoutSession:
    name: str
    exercise_type: SessionType
    exercises: list[Exercise] = field(default_factory=list)

    def add_exercise(self, exercise: Exercise):
        self.exercises.append(exercise)

    def add_exercises(self, list_of_exercises: list[Exercise]):
        self.exercises.extend(list_of_exercises)

    def remove_exercise(self, exercise: Exercise):
        self.exercises.remove(exercise)

    @staticmethod
    def move_exercise(self, exercise: Exercise, from_workout_type, to_workout_type):
        """Function for moving an exercise between workouts"""
        # Ideally this could be utilised within the front end; once the database is in use.
        # This may not be needed as the schema can just be updated backend in the construction of the backed datatypes
        pass

    @classmethod
    def get_exercises_by_type(cls, exercise_type: SessionType) -> list[Exercise]:
        return [exercise for exercise in cls.exercises if exercise.type == exercise_type]

    @staticmethod
    def to_string(session: "WorkoutSession") -> str:
        ...

    

#TODO, write DB to add exercises to DB. Ideally will be able to track and change weight and time targets.

#Seeding exercises:

#Back:
deadlifts = Exercise("Deadlifts", SessionType.BACK_CORE_ARMS, MuscleGroup.LOWER_BACK, weight=100, reps=5)
bent_over_rows = Exercise("Bent over rows", SessionType.BACK_CORE_ARMS, MuscleGroup.UPPER_BACK, weight=40, reps=10)
isolated_rows = Exercise("Isolated rows", SessionType.BACK_CORE_ARMS, MuscleGroup.UPPER_BACK, weight=24, reps=8)
reverse_fly = Exercise("Reverse fly", SessionType.BACK_CORE_ARMS, MuscleGroup.UPPER_BACK, weight=25, reps=10)
lat_pull_downs = Exercise("Lat pull downs", SessionType.BACK_CORE_ARMS, MuscleGroup.UPPER_BACK, weight=50, reps=10)

#Core:
crunches = Exercise("Crunches", SessionType.BACK_CORE_ARMS, MuscleGroup.CORE, reps=20)
weighted_situps = Exercise("Weighted Situps", SessionType.BACK_CORE_ARMS, MuscleGroup.CORE, weight=10, reps=12)

#Arms:
face_pulls = Exercise("Face-pulls", SessionType.BACK_CORE_ARMS, MuscleGroup.BICEP, weight=38, reps=10)
bicep_curls = Exercise("Bicep curls", SessionType.BACK_CORE_ARMS, MuscleGroup.BICEP, weight=8, reps=10)
barbell_bicep_curls = Exercise("Barbell bicep curls", SessionType.BACK_CORE_ARMS, MuscleGroup.BICEP, weight=25, reps=10)
pull_ups = Exercise("Pull ups", SessionType.BACK_CORE_ARMS, MuscleGroup.BICEP, reps=10)
skull_crushes = Exercise("Skull crushers", SessionType.BACK_CORE_ARMS, MuscleGroup.TRICEP, weight=10, reps=10)
dips = Exercise("Dips", SessionType.BACK_CORE_ARMS, MuscleGroup.TRICEP, reps=10)
tricep_pull_downs = Exercise("Tricep pull downs", SessionType.BACK_CORE_ARMS, MuscleGroup.TRICEP, weight=40, reps=10)
tricep_shoulder_lifts = Exercise("Tricep Shoulder Lifts", SessionType.BACK_CORE_ARMS, MuscleGroup.TRICEP, weight=20, reps=10)

#Chest:
bench_press = Exercise("Bench press", SessionType.CHEST_SHOULDERS, MuscleGroup.CHEST_PRESS, weight=50, reps=10)
press_ups = Exercise("Press ups", SessionType.CHEST_SHOULDERS, MuscleGroup.CHEST_PRESS, reps=15)
incline_press = Exercise("Incline press", SessionType.CHEST_SHOULDERS, MuscleGroup.CHEST_PRESS, weight=40, reps=10)
decline_press = Exercise("Decline press", SessionType.CHEST_SHOULDERS, MuscleGroup.CHEST_PRESS, weight=40, reps=10)
seated_press = Exercise("Seated press", SessionType.CHEST_SHOULDERS, MuscleGroup.CHEST_PRESS, weight=40, reps=10)
freeweight_fly = Exercise("Freeweight Fly", SessionType.CHEST_SHOULDERS, MuscleGroup.CHEST_FLY, weight=14, reps=10)
cable_fly = Exercise("Cable fly", SessionType.CHEST_SHOULDERS, MuscleGroup.CHEST_FLY, weight=50, reps=10)

#Shoulders:
side_shoulder_lifts = Exercise("Side shoulder lifts", SessionType.CHEST_SHOULDERS, MuscleGroup.SHOULDER_SIDE, weight=6, reps=10)
front_shoulder_lifts = Exercise("Front shoulder lifts", SessionType.CHEST_SHOULDERS, MuscleGroup.SHOULDER_SIDE, weight=10, reps=10)
standing_shoulder_press = Exercise("Standing Shoulder press", SessionType.CHEST_SHOULDERS, MuscleGroup.SHOULDER_PRESS, weight=30, reps=8)
seated_shoulder_press = Exercise("Seated Shoulder press", SessionType.CHEST_SHOULDERS, MuscleGroup.SHOULDER_PRESS, weight=25, reps=8)

#Legs:
squats = Exercise("Squats", SessionType.LEGS, MuscleGroup.WHOLE_LEG, weight=80, reps=8)
wall_sits = Exercise("Wall sits", SessionType.LEGS, MuscleGroup.WHOLE_LEG, time=30)
leg_curls = Exercise("Leg Curls", SessionType.LEGS, MuscleGroup.HAMSSTRINGS, weight=45, reps=10)
leg_extensions = Exercise("Leg extensions", SessionType.LEGS, MuscleGroup.QUADS, weight=55, reps=10)
leg_press = Exercise("Leg press", SessionType.LEGS, MuscleGroup.WHOLE_LEG, weight=120, reps=10)
lunges = Exercise("Lunges", SessionType.LEGS, MuscleGroup.GLUTES, weight=10, reps=12)
hungarian_split_squats = Exercise("Hungarian split squats", SessionType.LEGS, MuscleGroup.GLUTES, weight=10, reps=10)


#HIIT:
mountain_climbers = Exercise("Mountain climbers", SessionType.HIIT, MuscleGroup.CORE, time=30)
plank = Exercise("Plank", SessionType.HIIT, MuscleGroup.CORE, time=60)
interval_pressups = Exercise("Pressups", SessionType.HIIT, MuscleGroup.CHEST_PRESS, time=30)
interval_situps = Exercise("Situps", SessionType.HIIT, MuscleGroup.CORE, time=30)
box_jump = Exercise("boxjump", SessionType.HIIT, MuscleGroup.WHOLE_LEG, time=30)
paratroopers = Exercise("Paratroopers", SessionType.HIIT, MuscleGroup.UPPER_BACK, time=30)
side_plank = Exercise("Side plank", SessionType.HIIT, MuscleGroup.CORE, time=30)
raised_plank = Exercise("Raised plank", SessionType.HIIT, MuscleGroup.CORE, time=60)
shoulder_taps = Exercise("Shoulder taps", SessionType.HIIT, MuscleGroup.CORE, time=45)
reverse_crunches = Exercise("Reverse crunches", SessionType.HIIT, MuscleGroup.CORE, time=30)
bicycles = Exercise("Bicycles", SessionType.HIIT, MuscleGroup.CORE, time=30)
v_sits = Exercise("V-sits", SessionType.HIIT, MuscleGroup.CORE, time=30)
leg_raises = Exercise("Leg raises", SessionType.HIIT, MuscleGroup.CORE, time=30)
static_shoulder_lifts = Exercise("Static shoulder lifts", SessionType.HIIT, MuscleGroup.SHOULDER_SIDE, weight=4, time=30)
mobile_shoulder_lifts = Exercise("Mobile shoulder lifts", SessionType.HIIT, MuscleGroup.SHOULDER_SIDE, weight=6, time=30)
interval_bicep_curls = Exercise("Bicep curls", SessionType.HIIT, MuscleGroup.BICEP, weight=8, time=30)
interval_tricep_lifts = Exercise("Tricep lifts", SessionType.HIIT, MuscleGroup.TRICEP, weight=16, time=30)
interval_squats = Exercise("Squats", SessionType.HIIT, MuscleGroup.WHOLE_LEG, weight=40, time=30)
jumping_lunges = Exercise("Jumping Lunges", SessionType.HIIT, MuscleGroup.QUADS, time=30)

#Squats, Lunges, Push-ups, Plank, Sit-ups',
#Dips, Inverted rows, Russian twists, Mountain climbers, Side plank',
#Burpees, Single-leg squats, Close-grip push-ups, Bicycle crunches, Glute bridges',
#Incline push-ups, Jumping jacks, Plank jacks, Jump squats, V-ups',
#Rest day',
#Jumping lunges, Tricep dips, Box jumps, Superman plank, Bicycle crunches'


#Cardio:
fartlek_10 = Exercise("FARTLEK 10k", SessionType.CARDIO)
ten_k = Exercise("10K", SessionType.CARDIO)
five_k = Exercise("5K", SessionType.CARDIO, secondary_type=SessionType.REST)
hiit_workout = Exercise("HIIT workout", SessionType.CARDIO, secondary_type=SessionType.HIIT)
fartlek_5 = Exercise("FARTLEK 5k", SessionType.CARDIO, secondary_type=SessionType.REST)

#half_maraton = Exercise("Half marathon", SessionType.CARDIO)

#Rest:
Rest_Day = Exercise("Rest Day", SessionType.REST)


@dataclass
class HIIT:
    type: SessionType
    exercises: list[Exercise]

    @staticmethod
    def _get_plan():
        """Randomly generates a plan for a HIIT workout.
        Fills up to 15 exercises, to be done in a 30 active and 30 second rest.
        2 sets would provide a 30 minute workout."""

        #first copy the list of HIIT Exercises for use.
        exercise_pool = deepcopy(Exercise.HIIT)

        # Prev muscle_group to be stored for checks.
        prev_exercise_type = None

        # Loop counter to prevent infinity looping.
        loops = 0

        # Initialise list for plan to be filled by loop below.
        plan = []

        # Start plan filling:
        while len(plan) != 15:

            # Loop breaker if infinite loop caused.
            if loops > 30:
                return {"HIIT workout": plan}

            # Pick HIIT exercise
            chosen_exercise = random.choice(exercise_pool)

            # If the muscle group of the exercise is same as prev; discard.
            if chosen_exercise.muscle_group == prev_exercise_type:
                loops+=1
                continue


            else:
                # Add new exercise to plan.
                plan.append(chosen_exercise)

                # Set the MuscleGroup to ensure no muscle overload.
                prev_exercise_type = chosen_exercise.muscle_group

                # Remove exercise from pool to ensure isnt duplicated.
                exercise_pool.remove(chosen_exercise)

        return {"HIIT workout": plan} #TODO - timings?