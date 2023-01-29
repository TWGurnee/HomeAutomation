from pathlib import Path
import json

from .session_type import SessionType
from .muscle_group import MuscleGroup

"""This config constant allows to define the number of exercises of a specific muscle group to be associated with a specific gym days"""




#TODO Create class for config alteration:
#   -Init base config
#   -Change config
#   -Switch between 3 preset configs?
#   -

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



# CURRENT_CONFIG_FILE = Path(r"gym_config.json")

# def config_to_json(config_file):

# with open(CURRENT_CONFIG_FILE, 'w') as f:
#     json.dumps(GYM_DAY_CONFIG)


