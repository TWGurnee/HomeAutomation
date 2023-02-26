from enum import Enum

class MuscleGroup(Enum):
    # BACK_CORE_ARMS
    LOWER_BACK = "Lower Back"
    UPPER_BACK = "Upper Back"
    CORE = "Core"
    BICEP = "Bicep"
    TRICEP = "Tricep"
    #CHESTSHOULDERS
    CHEST_PRESS = "Chest Press"
    CHEST_FLY = "Chest Fly"
    SHOULDER_PRESS = "Shoulder Press"
    SHOULDER_SIDE = "Shoulder Side"
    #LEGS
    QUADS = "Quads"
    HAMSTRINGS = "Hamstrings"
    GLUTES = "Glutes"
    WHOLE_LEG = "Whole Leg"