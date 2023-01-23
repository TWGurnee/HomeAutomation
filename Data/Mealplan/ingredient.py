from dataclasses import dataclass


@dataclass(frozen=True)
class Ingredient:
    name: str
    quantity: int
    category: str

# Ingredient.categories:
# Meat (includes fish)
# Veg
# Frozen
# Beverages
# Long-life
# Dairy
# Condiment
# Bread
# Herbs/Spices