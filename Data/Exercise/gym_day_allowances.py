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

CURRENT_PLAN = 3
# Currently 4 does not work as there are no exercises stored with a day type of upper or lower, they are currently stored as 3 day SessionType


""" 3 gym 3 cardio plan """
def get_gym_config():
    if CURRENT_PLAN == 3:

        # To allow for a day gap between each gym session, below are all possible configurations indexes of the week.
        GYM_INDEXES = [
            [0,2,4],
            [0,2,5],
            [0,2,6],
            [0,3,5],
            [0,3,6],
            [0,4,6],
            [1,3,5],
            [1,3,6],
            [1,4,6],
            [2,4,6]
        ]

        # Week consists of: {Type of workout session: number of weekdays}
        WEEK_ALLOWANCES = {
            SessionType.BACK_CORE_ARMS: 1,
            SessionType.CHEST_SHOULDERS: 1,
            SessionType.LEGS: 1,
            SessionType.CARDIO: 3,
            SessionType.REST: 2
        }

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

        PLAN_CONFIG = (GYM_INDEXES, WEEK_ALLOWANCES, GYM_DAY_CONFIG) 
        return PLAN_CONFIG


    """4 day gym phase 1"""

    if CURRENT_PLAN == 4:

        #4 day indexes: includes one back to back day
        GYM_INDEXES = [
        [0,1,3,5],
        [0,1,3,6],
        [0,1,4,6],
        [0,2,3,5],
        [0,2,3,6],
        [0,2,4,5],
        [0,2,4,6],
        [0,2,5,6],
        [0,3,4,6],
        [0,3,5,6],
        [1,2,4,6],
        [1,3,4,6],
        [1,3,5,6]
        ]

        WEEK_ALLOWANCES = {
            SessionType.UPPER: 2,
            SessionType.LOWER: 2,
            SessionType.CARDIO: 1,
            SessionType.REST: 2
        }

        GYM_DAY_CONFIG = {

            SessionType.UPPER: (
                (MuscleGroup.UPPER_BACK, 1),
                (MuscleGroup.CHEST_PRESS, 1),
                (MuscleGroup.CHEST_FLY, 1),
                (MuscleGroup.SHOULDER_PRESS, 1),
                (MuscleGroup.SHOULDER_SIDE, 1),
                (MuscleGroup.BICEP, 2),
                (MuscleGroup.TRICEP, 2)
            ),

            SessionType.LOWER: (
                (MuscleGroup.CORE, 1),
                (MuscleGroup.LOWER_BACK, 1),
                (MuscleGroup.WHOLE_LEG, 3),
                (MuscleGroup.QUADS, 1),
                (MuscleGroup.HAMSTRINGS, 1),
                (MuscleGroup.GLUTES, 1)
            )

        }


        PLAN_CONFIG = (GYM_INDEXES, WEEK_ALLOWANCES, GYM_DAY_CONFIG) 
        return PLAN_CONFIG







# CURRENT_CONFIG_FILE = Path(r"gym_config.json")

# def config_to_json(config_file):

# with open(CURRENT_CONFIG_FILE, 'w') as f:
#     json.dumps(GYM_DAY_CONFIG)


