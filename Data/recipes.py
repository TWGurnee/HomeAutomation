from dataclasses import dataclass

@dataclass(frozen=True)
class Ingredient:
    name: str
    quantity: int
    category: str
    choices: list[str]=None

    def __hash__(self):
        # Create a hash value based on the name, quantity, and category of the ingredient
        # You could use any combination of these attributes or add more attributes to the hash if needed
        return hash((self.name, self.quantity, self.category))

@dataclass
class Recipe:
    name: str
    ingredients: list[Ingredient]
    type: str
    All_Recipes = []

    def __post_init__(self):
        self.__class__.All_Recipes.append(self)

#### Food Ideas Section ####
"""
- Roast shrimp and veggie salad
- More Salads & healthy options
"""

# Recipes list:

# Tim's Meals

Burritos = Recipe(
    name='Burritos',
    ingredients=[
        Ingredient(name='Mince/Chicken', quantity=1, category="Meat", choices=['Mince', 'Chicken']),
        Ingredient(name='Onions', quantity=1, category="Veg"),
        Ingredient(name='Peppers', quantity=1, category="Veg"),
        Ingredient(name='Wraps', quantity=1, category="Bread"),
        Ingredient(name='Cheddar', quantity=1, category="Dairy"), 
        Ingredient(name='Avocado', quantity=1, category="Veg"), 
        Ingredient(name='Mushrooms', quantity=1, category="Veg"), 
        Ingredient(name='Leaves', quantity=1, category="Veg"), 
        Ingredient(name='Rice', quantity=1, category="Long-life"), 
        Ingredient(name='Garlic', quantity=1, category="Veg")
        ],
    type='Tim')

Indian_Curry = Recipe(
    name='Indian Curry',
    ingredients=[
        Ingredient(name='Curry Paste', quantity=1, category='Herbs/Spices'),
        Ingredient(name='Peppers', quantity=1, category='Veg'),
        Ingredient(name='Onions', quantity=1, category='Veg'),
        Ingredient(name='Mushrooms', quantity=1, category='Veg'),
        Ingredient(name='Rice', quantity=1, category='Long-life'),
        Ingredient(name='Naan', quantity=1, category='Bread'),
        Ingredient(name='Chutney', quantity=1, category='Condiment'),
        Ingredient(name='Yoghurt/Cream', quantity=1, category='Dairy', choices=['Yoghurt', 'Cream'])
        ],
    type='Tim')

Arrabiata = Recipe(
    name='Arrabiata',
    ingredients=[
        Ingredient(name='Chopped Tomatoes', quantity=1, category='Veg'),
        Ingredient(name='Penne', quantity=1, category='Long-life'), 
        Ingredient(name='Basil', quantity=1, category='Herbs/Spices'), 
        Ingredient(name='Chili', quantity=1, category='Herbs/Spices'), 
        Ingredient(name='Onions', quantity=1, category='Veg'), 
        Ingredient(name='Peppers', quantity=1, category='Veg'),
        Ingredient(name='Mushrooms', quantity=1, category='Veg'), 
        Ingredient(name='Oregano', quantity=1, category='Herbs/Spices')
        ],
    type='Tim')

Thai_Curry = Recipe(
    name='Thai Curry',
    ingredients=[
        Ingredient(name='Coconut Milk', quantity=1, category='Long-life'),
        Ingredient(name='Broccoli', quantity=1, category='Frozen'),
        Ingredient(name='Leaves', quantity=1, category='Veg'),
        Ingredient(name='Green Beans', quantity=1, category='Frozen'),
        Ingredient(name='Peas', quantity=1, category='Frozen'),
        Ingredient(name='Chicken', quantity=1, category='Meat'),
        Ingredient(name='Prawn Crackers', quantity=1, category='Snacks'),
        Ingredient(name='Onions', quantity=1, category='Veg')
        ],
    type='Tim')

Burgers = Recipe(
    name='Burgers',
    ingredients=[
        Ingredient(name='Mince', quantity=1, category='Meat'),
        Ingredient(name='Bread Rolls', quantity=1, category='Bread'),
        Ingredient(name='Beef Tomato', quantity=1, category='Veg'),
        Ingredient(name='Lettuce', quantity=1, category='Veg'), 
        Ingredient(name='Mustard', quantity=1, category='Condiment'), 
        Ingredient(name='Parsley', quantity=1, category='Herbs/Spices'), 
        Ingredient(name='Ketchup', quantity=1, category='Condiment'), 
        Ingredient(name='Mayonnaise', quantity=1, category='Condiment'), 
        Ingredient(name='Chips', quantity=1, category='Frozen'), 
        Ingredient(name='Onions', quantity=1, category='Veg'), 
        Ingredient(name='Garlic', quantity=1, category='Veg')
        ],
    type='Tim')  

Pizza = Recipe(
    name='Pizza',
    ingredients=[
        Ingredient(name='Flatbread', quantity=1, category='Bread'), 
        Ingredient(name='Mozzarella', quantity=1, category='Dairy'), 
        Ingredient(name='Parmesan', quantity=1, category='Dairy'), 
        Ingredient(name='Meat Topping', quantity=1, category='Meat', choices=['Pepperoni', 'Chicken', 'Prosciutto']), 
        Ingredient(name='Mushrooms', quantity=1, category='Veg'),
        Ingredient(name='Peppers', quantity=1, category='Veg'),
        Ingredient(name='Tomato Puree', quantity=1, category='Long-life')
        ],
    type='Tim')

Steak = Recipe(
    name='Steak',
    ingredients=[
        Ingredient(name='Steak', quantity=1, category='Meat'),
        Ingredient(name='Broccoli/Asparagus', quantity=1, category='Veg', choices=['Broccoli', 'Asparagus']),
        Ingredient(name='Chips/Potatoes', quantity=1, category='Veg', choices=['Potatoes', 'Chips']),
        Ingredient(name='Peppercorn Sauce', quantity=1, category='Condiment')
        ],
    type='Tim')

Quesadillas = Recipe(
    name='Quesadillas',
    ingredients=[
        Ingredient(name='Wraps', quantity=1, category='Bread'),
        Ingredient(name='Chicken', quantity=1, category='Meat'),
        Ingredient(name='Mushroom', quantity=1, category='Veg'),
        Ingredient(name='Cheddar', quantity=1, category='Dairy'),
        Ingredient(name='Onions', quantity=1, category='Veg'),
        Ingredient(name='Leaves', quantity=1, category='Veg')
        ],
    type='Tim')

Cramy_Pesto = Recipe(
    name='Creamy Pesto',
    ingredients=[
        Ingredient(name='Fusilli', quantity=1, category='Long-life'),
        Ingredient(name='Pesto', quantity=1, category='Long-life'),
        Ingredient(name='Cherry Tomatoes', quantity=1, category='Veg'),
        Ingredient(name='Parmesan', quantity=1, category='Dairy'),
        Ingredient(name='Olive Oil', quantity=1, category='Long-life'),
        Ingredient(name='Double Cream', quantity=1, category='Dairy'),
        Ingredient(name='Basil', quantity=1, category='Herbs/Spices'),
        Ingredient(name='Oregano', quantity=1, category='Herbs/Spices')
        ],
    type='Tim')

Stir_Fry = Recipe(
    name='Stir Fry',
    ingredients=[
        Ingredient(name='Stir Fry Sauce', quantity=1, category='Condiment'),
        Ingredient(name='Soy Sauce', quantity=1, category='Condiment'),
        Ingredient(name='Noodles', quantity=1, category='Long-life'),
        Ingredient(name='Mini-Corn', quantity=1, category='Veg'),
        Ingredient(name='Beansprouts', quantity=1, category='Veg'),
        Ingredient(name='Mushrooms', quantity=1, category='Veg'),
        Ingredient(name='Chicken/Steak', quantity=1, category='Meat', choices=['Chicken', 'Steak'])
        ],
    type='Tim')

# Freya's Meals

Mac_and_Cheese = Recipe(
    name='Mac & Cheese',
    ingredients=[
        Ingredient(name='Macaroni', quantity=1, category='Long-life'),
        Ingredient(name='Butter', quantity=1, category='Dairy'),
        Ingredient(name='Milk', quantity=1, category='Dairy'),
        Ingredient(name='Cheddar', quantity=1, category='Dairy')
        ],
    type='Freya')

Sausage_Pasta_Bake = Recipe(
    name='Sausage Pasta Bake',
    ingredients=[
        Ingredient(name='Red Wine', quantity=1, category='Beverages'),
        Ingredient(name='Rigatoni', quantity=1, category='Long-life'),
        Ingredient(name='Sausages', quantity=1, category='Meat'),
        Ingredient(name='Carrots', quantity=1, category='Veg'),
        Ingredient(name='Onions', quantity=1, category='Veg'),
        Ingredient(name='Tomato Puree', quantity=1, category='Long-life'),
        Ingredient(name='Veg Stock', quantity=1, category='Long-life'),
        Ingredient(name='Milk', quantity=1, category='Dairy'),
        Ingredient(name='Flour', quantity=1, category='Long-life'),
        Ingredient(name='Cheese', quantity=1, category='Dairy'),
        Ingredient(name='Rosemary', quantity=1, category='Herbs/Spices'),
        Ingredient(name='Basil', quantity=1, category='Herbs/Spices')
        ],
    type='Freya')

Chicken_Pie = Recipe(
    name='Chicken Pie',
    ingredients=[
        Ingredient(name='Chicken', quantity=1, category='Meat'),
        Ingredient(name='Pastry', quantity=1, category='Long-life'), 
        Ingredient(name='Onions', quantity=1, category='Veg'), 
        Ingredient(name='Flour', quantity=1, category='Long-life'), 
        Ingredient(name='Milk', quantity=1, category='Dairy'), 
        Ingredient(name='Chicken Stock', quantity=1, category='Long-life'), 
        Ingredient(name='White Wine', quantity=1, category='Beverages'), 
        Ingredient(name='Potatoes', quantity=1, category='Veg'), 
        Ingredient(name='Thyme', quantity=1, category='Herbs/Spices'), 
        Ingredient(name='Basil', quantity=1, category='Herbs/Spices'), 
        Ingredient(name='Leeks', quantity=1, category='Veg')
        ],
    type='Freya')

Salmon_Tagiatelle = Recipe(
    name='Salmon Tagiatelle',
    ingredients=[
        Ingredient(name='Salmon', quantity=1, category='Meat'),
        Ingredient(name='Mushroom', quantity=1, category='Veg'), 
        Ingredient(name='Crème fraiche', quantity=1, category='Dairy'), 
        Ingredient(name='Salt', quantity=1, category='Herbs/Spices'), 
        Ingredient(name='Pepper', quantity=1, category='Herbs/Spices'),  
        Ingredient(name='Lemon Juice', quantity=1, category='Condiment')
        ],
    type='Freya')

Chicken_Stew = Recipe(
    name='Chicken Stew',
    ingredients=[
        Ingredient(name='Chicken Thighs', quantity=1, category='Meat'),
        Ingredient(name='Dijon Mustard', quantity=1, category='Condiment'),
        Ingredient(name='Crème fraiche', quantity=1, category='Dairy'),
        Ingredient(name='Veg Stock', quantity=1, category='Long-life'),
        Ingredient(name='Chicken Stock', quantity=1, category='Long-life'),
        Ingredient(name='Butter', quantity=1, category='Dairy'), 
        Ingredient(name='Parsley', quantity=1, category='Herbs/Spices'), 
        Ingredient(name='Peas', quantity=1, category='Frozen'), 
        Ingredient(name='Leeks', quantity=1, category='Veg'), 
        Ingredient(name='Celery', quantity=1, category='Veg'), 
        Ingredient(name='Potatoes', quantity=1, category='Veg')
        ],
    type='Freya')

Baked_Potatoes = Recipe(
    name='Baked Potatoes',
    ingredients=[
        Ingredient(name='Baked Potatoes', quantity=1, category='Veg'), 
        Ingredient(name='Tuna', quantity=1, category='Meat'), 
        Ingredient(name='Mayonnaise', quantity=1, category='Condiment'), 
        Ingredient(name='Baked Beans', quantity=1, category='Long-life'), 
        Ingredient(name='Leaves', quantity=1, category='Veg'),
        Ingredient(name='Butter', quantity=1, category='Dairy')
        ],
    type='Freya')

Salmon_Fillet = Recipe(
    name='Salmon Fillet', 
    ingredients=[
        Ingredient(name='Salmon', quantity=1, category='Meat'), 
        Ingredient(name='Potatoes', quantity=1, category='Veg'),
        Ingredient(name='Broccoli/Asparagus', quantity=1, category='Veg', choices=['Broccoli', 'Asparagus']),
        Ingredient(name='Butter', quantity=1, category='Dairy'), 
        Ingredient(name='Oregano', quantity=1, category='Herbs/Spices'),
        Ingredient(name='Chili Flakes', quantity=1, category='Herbs/Spices'), 
        Ingredient(name='Garlic', quantity=1, category='Veg')
        ], 
    type='Freya')

Harissa_Pasta = Recipe(
    name='Harissa Pasta',
    ingredients=[
        Ingredient(name='Rigatoni', quantity=1, category='Long-life'),
        Ingredient(name='Rose Harissa Paste', quantity=1, category='Herbs/Spices'),
        Ingredient(name='Mascarpone', quantity=1, category='Dairy'),
        Ingredient(name='Sundried Tomato', quantity=1, category='Veg'),
        Ingredient(name='Parmesan', quantity=1, category='Dairy'),
        Ingredient(name='Garlic', quantity=1, category='Veg'),
        Ingredient(name='Fresh Basil', quantity=1, category='Herbs/Spices')
        ],
    type='Freya')

Chicken_Alfredo = Recipe(
    name='Chicken Alfredo', 
    ingredients=[
        Ingredient(name='Penne', quantity=1, category='Long-life'), 
        Ingredient(name='Low Fat Cream Cheese', quantity=1, category='Dairy'), 
        Ingredient(name='Parmesan', quantity=1, category='Dairy'), 
        Ingredient(name='Oat Milk', quantity=1, category='Dairy'), 
        Ingredient(name='Flour', quantity=1, category='Long-life'), 
        Ingredient(name='Garlic', quantity=1, category='Veg'), 
        Ingredient(name='Butter', quantity=1, category='Dairy'), 
        Ingredient(name='Spinach', quantity=1, category='Veg')
        ], 
    type='Freya')

Katsu_Curry = Recipe(
    name='Katsu Curry', 
    ingredients=[
        Ingredient(name='Chicken', quantity=1, category='Meat'), 
        Ingredient(name='Breadcrumbs', quantity=1, category='Long-life'), 
        Ingredient(name='Rice', quantity=1, category='Long-life'), 
        Ingredient(name='Onions', quantity=1, category='Veg'), 
        Ingredient(name='Garlic', quantity=1, category='Veg'), 
        Ingredient(name='Ginger', quantity=1, category='Veg'), 
        Ingredient(name='Turmeric', quantity=1, category='Herbs/Spices'), 
        Ingredient(name='Mild Curry Powder', quantity=1, category='Herbs/Spices'), 
        Ingredient(name='Flour', quantity=1, category='Long-life'), 
        Ingredient(name='Veg Stock', quantity=1, category='Long-life'), 
        Ingredient(name='Coconut Milk', quantity=1, category='Long-life'), 
        Ingredient(name='Eggs', quantity=1, category='Dairy'), 
        Ingredient(name='Leaves', quantity=1, category='Veg')
        ], 
    type='Freya')

# Healthy Meals

Chicken_Avocado_Salad = Recipe(
    name='Chicken Avocado Salad',
    ingredients=[
        Ingredient(name='Chicken', quantity=1, category='Meat'), 
        Ingredient(name='Leaves', quantity=1, category='Veg'),
        Ingredient(name='Avocado', quantity=1, category='Veg'),
        Ingredient(name='Onions', quantity=1, category='Veg'),
        Ingredient(name='Peppers', quantity=1, category='Veg'),
        Ingredient(name='Cucumber', quantity=1, category='Veg'),
        Ingredient(name='Honey Mustard Dressing', quantity=1, category='Condiment')
        ],
    type='Healthy')

Cod_Mango_Salad = Recipe(
    name='Cod Mango Salad', 
    ingredients=[
        Ingredient(name='Cod', quantity=1, category='Meat'), 
        Ingredient(name='Mango', quantity=1, category='Veg'), 
        Ingredient(name='Leaves', quantity=1, category='Veg'), 
        Ingredient(name='Avocado', quantity=1, category='Veg')
        ],
    type='Healthy')

Halloumi_Mango_Salad = Recipe(
    name='Halloumi & Mango Salad', 
    ingredients=[
        Ingredient(name='Halloumi', quantity=1, category='Dairy'), 
        Ingredient(name='Mango', quantity=1, category='Veg'), 
        Ingredient(name='Rocket', quantity=1, category='Veg'), 
        Ingredient(name='Cherry Tomato', quantity=1, category='Veg')
        ],
    type='Healthy')

Greek_Salad = Recipe(
    name='Greek Salad', 
    ingredients=[
        Ingredient(name='Feta', quantity=1, category='Dairy'), 
        Ingredient(name='Leaves', quantity=1, category='Veg'), 
        Ingredient(name='Olives', quantity=1, category='Veg'), 
        Ingredient(name='Cucumber', quantity=1, category='Veg'), 
        Ingredient(name='Sundried Tomato', quantity=1, category='Veg'), 
        Ingredient(name='Olive Oil', quantity=1, category='Long-life'), 
        Ingredient(name='Balsamic Vinegar', quantity=1, category='Condiment')
        ],
    type='Healthy')

CousCous_Honey_Garlic_Prawns = Recipe(
    name='CousCous Honey Garlic Prawns',
    ingredients=[
        Ingredient(name='Prawns', quantity=1, category='Frozen'),
        Ingredient(name='Honey', quantity=1, category='Long-life'),
        Ingredient(name='Cous Cous', quantity=1, category='Long-life'),
        Ingredient(name='Garlic', quantity=1, category='Veg'), 
        Ingredient(name='Asparagus', quantity=1, category='Veg'),
        Ingredient(name='Peppers', quantity=1, category='Veg')
        ],
    type='Healthy')