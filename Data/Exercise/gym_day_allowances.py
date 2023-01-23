from .session_type import SessionType
from .muscle_group import MuscleGroup


"""This config constant allows to define the number of exercises of a specific muscle group to be associated with a specific gym days"""

GYM_DAY_CONFIG = {

    SessionType.BACK_CORE_ARMS: (
        (MuscleGroup.UPPER_BACK, 2),
        (MuscleGroup.LOWER_BACK, 1),
        (MuscleGroup.CORE, 1),
        (MuscleGroup.BICEP, 2),
        (MuscleGroup.TRICEP, 2)
    ),

    SessionType.CHEST_SHOULDERS: (
        (MuscleGroup.CHEST_PRESS, 3),
        (MuscleGroup.CHEST_FLY, 2),
        (MuscleGroup.SHOULDER_PRESS, 2),
        (MuscleGroup.SHOULDER_SIDE, 2)
    ),
    
    SessionType.LEGS: (
        (MuscleGroup.WHOLE_LEG, 3),
        (MuscleGroup.QUADS, 1),
        (MuscleGroup.HAMSTRINGS, 1),
        (MuscleGroup.GLUTES, 1)
    ),
}