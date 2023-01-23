from enum import Enum

class SessionType(Enum):
    BACK_CORE_ARMS = "Back Core Arm day"
    CHEST_SHOULDERS = "Chest Shoulder day"
    LEGS = "Leg day"
    CARDIO = "Cardio day"
    HIIT = "HIIT workout"
    REST = "Rest day"