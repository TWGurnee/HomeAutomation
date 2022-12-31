from dataclasses import dataclass, field
from enum import Enum
import random


class ExerciseType(Enum):
    BACK_CORE_ARMS = 1
    CHEST_SHOULDERS = 2
    LEGS = 3
    CARDIO = 4
    HIIT = 5


class MuscleGroup(Enum):
    # BACK_CORE_ARMS
    LOWER_BACK = 1
    UPPER_BACK = 2
    CORE = 3
    BICEP = 4
    TRICEP = 5
    #CHESTSHOULDERS
    CHEST = 6
    SHOULDERS = 7
    #LEGS
    QUADS = 8
    HAMSSTRINGS = 9
    GLUTES = 10
    WHOLE_LEG = 11


@dataclass
class Exercise:
    name: str
    type: ExerciseType
    muscle_group: MuscleGroup = field(default=None, metadata={"description": "The group of muscles used in the exercise. Required to ensure a balanced workout"})
    weight: int = field(default=None, metadata={"description": "Weight in Kg used for the exercise"})
    reps: int = field(default=None, metadata={"description": "Number of reps to perform for the exercise"})
    time: int = field(default=None, metadata={"description": "Field for the best time, target time, or input time. Measured in seconds"})
    #sets: int = field(default_factory=lambda: 4)

    Back_Core_Arm_Day = []
    Chest_Shoulder_Day = []
    Leg_Day = []
    Cardio = []
    HIIT = []

    @staticmethod 
    def init_lists(): # supposedly required to ensure only one copy of each list is stored in memory.
        Exercise.Back_Core_Arm_Day = []
        Exercise.Chest_Shoulder_Day = []
        Exercise.Leg_Day = []
        Exercise.Cardio = []
        Exercise.HIIT = []

    def __post_init__(self):
        if not Exercise.Back_Core_Arm_Day:
            Exercise.init_lists() #### Not sure if required
        if self.type == ExerciseType.BACK_CORE_ARMS:
            self.Back_Core_Arm_Day.append(self)
        elif self.type == ExerciseType.CHEST_SHOULDERS:
            self.Chest_Shoulder_Day.append(self)
        elif self.type == ExerciseType.LEGS:
            self.Leg_Day.append(self)
        elif self.type == ExerciseType.CARDIO:
            self.Cardio.append(self)
        elif self.type == ExerciseType.HIIT:
            self.HIIT.append(self)


#TODO, write DB to add exercises to DB. Ideally will be able to track and change weight and time targets.


#Seeding exercises:

#Back:
deadlifts = Exercise("Deadlifts", ExerciseType.BACK_CORE_ARMS, MuscleGroup.LOWER_BACK, weight=100, reps=5)
bent_over_rows = Exercise("Bent over rows", ExerciseType.BACK_CORE_ARMS, MuscleGroup.UPPER_BACK, weight=40, reps=10)
isolated_rows = Exercise("Isolated rows", ExerciseType.BACK_CORE_ARMS, MuscleGroup.UPPER_BACK, weight=24, reps=8)
reverse_fly = Exercise("Reverse fly", ExerciseType.BACK_CORE_ARMS, MuscleGroup.UPPER_BACK, weight=25, reps=10)
lat_pull_downs = Exercise("Lat pull downs", ExerciseType.BACK_CORE_ARMS, MuscleGroup.UPPER_BACK, weight=50, reps=10)

#Core:
crunches = Exercise("Crunches", ExerciseType.BACK_CORE_ARMS, MuscleGroup.CORE, reps=20)
weighted_situps = Exercise("Weighted Situps", ExerciseType.BACK_CORE_ARMS, MuscleGroup.CORE, weight=10, reps=12)

#Arms:
face_pulls = Exercise("Face-pulls", ExerciseType.BACK_CORE_ARMS, MuscleGroup.BICEP, weight=38, reps=10)
bicep_curls = Exercise("Bicep curls", ExerciseType.BACK_CORE_ARMS, MuscleGroup.BICEP, weight=8, reps=10)
barbell_bicep_curls = Exercise("Barbell bicep curls", ExerciseType.BACK_CORE_ARMS, MuscleGroup.BICEP, weight=25, reps=10)
pull_ups = Exercise("Pull ups", ExerciseType.BACK_CORE_ARMS, MuscleGroup.BICEP, reps=10)
skull_crushes = Exercise("Skull crushers", ExerciseType.BACK_CORE_ARMS, MuscleGroup.TRICEP, weight=10, reps=10)
dips = Exercise("Dips", ExerciseType.BACK_CORE_ARMS, MuscleGroup.TRICEP, reps=10)
tricep_pull_downs = Exercise("Tricep pull downs", ExerciseType.BACK_CORE_ARMS, MuscleGroup.TRICEP, weight=40, reps=10)
tricep_shoulder_lifts = Exercise("Tricep Shoulder Lifts", ExerciseType.BACK_CORE_ARMS, MuscleGroup.TRICEP, weight=20, reps=10)

#Chest:
bench_press = Exercise("Bench press", ExerciseType.CHEST_SHOULDERS, MuscleGroup.CHEST, weight=50, reps=10)
press_ups = Exercise("Press ups", ExerciseType.CHEST_SHOULDERS, MuscleGroup.CHEST, reps=15)
incline_press = Exercise("Incline press", ExerciseType.CHEST_SHOULDERS, MuscleGroup.CHEST, weight=40, reps=10)
decline_press = Exercise("Decline press", ExerciseType.CHEST_SHOULDERS, MuscleGroup.CHEST, weight=40, reps=10)
seated_press = Exercise("Seated press", ExerciseType.CHEST_SHOULDERS, MuscleGroup.CHEST, weight=40, reps=10)
freeweight_fly = Exercise("Freeweight Fly", ExerciseType.CHEST_SHOULDERS, MuscleGroup.CHEST, weight=14, reps=10)
cable_fly = Exercise("Cable fly", ExerciseType.CHEST_SHOULDERS, MuscleGroup.CHEST, weight=50, reps=10)

#Shoulders:
side_shoulder_lifts = Exercise("Side shoulder lifts", ExerciseType.CHEST_SHOULDERS, MuscleGroup.SHOULDERS, weight=6, reps=10)
front_shoulder_lifts = Exercise("Front shoulder lifts", ExerciseType.CHEST_SHOULDERS, MuscleGroup.SHOULDERS, weight=10, reps=10)
standing_shoulder_press = Exercise("Standing Shoulder press", ExerciseType.CHEST_SHOULDERS, MuscleGroup.SHOULDERS, weight=30, reps=8)
seated_shoulder_press = Exercise("Seated Shoulder press", ExerciseType.CHEST_SHOULDERS, MuscleGroup.SHOULDERS, weight=25, reps=8)

#Legs:
squats = Exercise("Squats", ExerciseType.LEGS, MuscleGroup.WHOLE_LEG, weight=80, reps=8)
wall_sits = Exercise("Wall sits", ExerciseType.LEGS, MuscleGroup.WHOLE_LEG, time=30)
leg_curls = Exercise("Leg Curls", ExerciseType.LEGS, MuscleGroup.HAMSSTRINGS, weight=45, reps=10)
leg_extensions = Exercise("Leg extensions", ExerciseType.LEGS, MuscleGroup.QUADS, weight=55, reps=10)
leg_press = Exercise("Leg press", ExerciseType.LEGS, MuscleGroup.WHOLE_LEG, weight=120, reps=10)
lunges = Exercise("Lunges", ExerciseType.LEGS, MuscleGroup.GLUTES, weight=10, reps=12)
hungarian_split_squats = Exercise("Hungarian split squats", ExerciseType.LEGS, MuscleGroup.GLUTES, weight=10, reps=10)


#HIIT:
mountain_climbers = Exercise("Mountain climbers", ExerciseType.HIIT, MuscleGroup.CORE, time=30)
plank = Exercise("Plank", ExerciseType.HIIT, MuscleGroup.CORE, time=60)
interval_pressups = Exercise("Pressups", ExerciseType.HIIT, MuscleGroup.CHEST, time=30)
interval_situps = Exercise("Situps", ExerciseType.HIIT, MuscleGroup.CORE, time=30)
box_jump = Exercise("boxjump", ExerciseType.HIIT, MuscleGroup.WHOLE_LEG, time=30)
paratroopers = Exercise("Paratroopers", ExerciseType.HIIT, MuscleGroup.UPPER_BACK, time=30)
side_plank = Exercise("Side plank", ExerciseType.HIIT, MuscleGroup.CORE, time=30)
raised_plank = Exercise("Raised plank", ExerciseType.HIIT, MuscleGroup.CORE, time=60)
shoulder_taps = Exercise("Shoulder taps", ExerciseType.HIIT, MuscleGroup.CORE, time=45)
reverse_crunches = Exercise("Reverse crunches", ExerciseType.HIIT, MuscleGroup.CORE, time=30)
bicycles = Exercise("Bicycles", ExerciseType.HIIT, MuscleGroup.CORE, time=30)
v_sits = Exercise("V-sits", ExerciseType.HIIT, MuscleGroup.CORE, time=30)
leg_raises = Exercise("Leg raises", ExerciseType.HIIT, MuscleGroup.CORE, time=30)
static_shoulder_lifts = Exercise("Static shoulder lifts", ExerciseType.HIIT, MuscleGroup.SHOULDERS, weight=4, time=30)
mobile_shoulder_lifts = Exercise("Mobile shoulder lifts", ExerciseType.HIIT, MuscleGroup.SHOULDERS, weight=6, time=30)
interval_bicep_curls = Exercise("Bicep curls", ExerciseType.HIIT, MuscleGroup.BICEP, weight=8, time=30)
interval_tricep_lifts = Exercise("Tricep lifts", ExerciseType.HIIT, MuscleGroup.TRICEP, weight=16, time=30)
interval_squats = Exercise("Squats", ExerciseType.HIIT, MuscleGroup.WHOLE_LEG, weight=40, time=30)
jumping_lunges = Exercise("Jumping Lunges", ExerciseType.HIIT, MuscleGroup.QUADS, time=30)

#Cardio:
five_k = Exercise("5K", ExerciseType.CARDIO)
ten_k = Exercise("10K", ExerciseType.CARDIO)
hiit_workout = Exercise("HIIT workout", ExerciseType.CARDIO)
fartlek_5 = Exercise("FARTLEK 5k", ExerciseType.CARDIO)
fartlek_10 = Exercise("FARTLEK 10k", ExerciseType.CARDIO)
#half_maraton = Exercise("Half marathon", ExerciseType.CARDIO)


@dataclass
class HIIT:
    type: ExerciseType
    exercises: list[Exercise]

    @staticmethod
    def _get_plan():
        HIIT.exercises = random.sample(Exercise.HIIT, 10)
        plan = [exercise.name for exercise in HIIT.exercises]
        return plan