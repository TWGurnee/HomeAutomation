from dataclasses import dataclass

from .session_type import SessionType
from .exercise import Exercise

#Currently unused
@dataclass
class HIIT:
    type: SessionType
    exercises: list[Exercise]