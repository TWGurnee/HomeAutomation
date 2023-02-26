from enum import Enum

class SessionType(Enum):
    # Standard
    CARDIO = "Cardio day"
    HIIT = "HIIT workout"
    REST = "Rest day"

    # 3 day per week
    BACK_CORE_ARMS = "Back Core Arm day"
    CHEST_SHOULDERS = "Chest Shoulder day"
    LEGS = "Leg day"

    # 4 day per week
    UPPER = "Upper Body"
    LOWER = "Lower Body"