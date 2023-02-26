from dataclasses import dataclass

from .ingredient import Ingredient

@dataclass(frozen=True)
class Recipe:
    name: str
    ingredients: list[Ingredient]
    type: str

#### Food Ideas ####
"""
- Roast shrimp and veggie salad
- More Salads & healthy options
"""