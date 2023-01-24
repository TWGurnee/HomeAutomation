import json

from dataclasses import dataclass, field, asdict, astuple, replace
from enum import Enum

from .session_type import SessionType
from .muscle_group import MuscleGroup


@dataclass
class Exercise:
    name: str
    type: SessionType
    muscle_group: MuscleGroup = field(default=None, metadata={"description": "The group of muscles used in the exercise. Required to ensure a balanced workout"}) #type: ignore
    weight: int = field(default=None, metadata={"description": "Weight in Kg used for the exercise"}) #type: ignore
    weight_increment: float = field(default=None, metadata={"description": "The weight in KG that the proposed exercise would be increased by when the target is met"}) #type: ignore
    reps: int = field(default=None, metadata={"description": "Number of reps to perform for the exercise"}) #type: ignore
    time: int = field(default=None, metadata={"description": "Field for the best time, target time, or input time. Measured in seconds"}) #type: ignore
    secondary_type: SessionType = field(default=None, metadata={"description": "The secondary type of an exercise. Current use cases are HIIT and 5K to allow for appropriate plan generation"}) #type: ignore
    #sets: int = field(default_factory=lambda: 4)


    @staticmethod
    def custom_asdict_factory(data):

        def convert_value(obj):
            if isinstance(obj, Enum):
                return obj.value
            return obj

        return dict((k, convert_value(v)) for k, v in data)

    def to_dict(self) -> dict:
        return asdict(self, dict_factory=Exercise.custom_asdict_factory)

    @staticmethod #TODO update to ensure works correctly
    def from_dict(data: dict) -> "Exercise":
        # We require a convert function as per the to_dict function to ensure the Enums are correclty initisalised prior to replace function.
        return replace(Exercise, **data) #type: ignore


    @staticmethod
    def custom_astuple_factory(data):

        def convert_value(obj):
            if isinstance(obj, Enum):
                return obj.value
            return obj

        return tuple(convert_value(i) for i in data)

    def to_tuple(self) -> tuple:
        return astuple(self, tuple_factory=Exercise.custom_astuple_factory)


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

    @staticmethod
    def from_dict_to_str(saved_json: "dict") -> str:
        output = ""
        output += f'\n- {saved_json["name"]}\n'
        if saved_json["weight"]: output += f'{saved_json["weight"]}kg,'
        if saved_json["reps"]: output += f' for {saved_json["reps"]} reps.'
        if saved_json["time"]: output += f' for {saved_json["time"]} seconds'
        return output
