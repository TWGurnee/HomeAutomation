from dataclasses import dataclass, field


@dataclass(frozen=True)
class Ingredient:
    name: str
    category: str
    quantity: int = field(default=None) #type: ignore
    unit: str = field(default=None) #type: ignore

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