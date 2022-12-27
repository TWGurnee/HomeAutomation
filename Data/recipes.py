from dataclasses import dataclass


@dataclass(frozen=True)
class Ingredient:
    name: str
    quantity: int
    category: str

    All_Ingredients = []

    def __post_init__(self):
        self.__class__.All_Ingredients.append(self)

    def __hash__(self): # Currently Unused
        # Create a hash value based on the name, quantity, and category of the ingredient
        # You could use any combination of these attributes or add more attributes to the hash if needed
        return hash((self.name, self.quantity, self.category))


def categorise_ingredient(ingredient: Ingredient) -> str:
    """Get or assign category for a ingredient.name or string"""
    
    # To get categories we need all current ingredients and their category.
    all_ingredient_names = [ingredient.name for ingredient in Ingredient.All_Ingredients]
    get_category_from_name = {i.name: i.category for i in Ingredient.All_Ingredients}
    
    # Categorise ingredient
    if ingredient in all_ingredient_names:
        category = get_category_from_name[ingredient]
    else:
        category = "UNCATEGORISED"
    
    return category


@dataclass
class Recipe:
    name: str
    ingredients: list[Ingredient]
    type: str

    All_Recipes = []

    def __post_init__(self):
        self.__class__.All_Recipes.append(self)

    @staticmethod
    def generate_recipe(recipe_dict: dict):
        """Helper method to generate recipes from a simple typed input dict:
        For example: 
        `Test_Recipe = {('Tim', 'Steak'): ['Steak', 'Broccoli/Asparagus', 'Chips/Potatoes', 'Peppercorn Sauce']}`
        `generate_recipe(Test_Recipe)`
        Would give the steak recipe reflected below. 
        Currently result is unformatted and works on dicts of 1 recipe"""

        # Unpack input:
        meal_type, name = list(recipe_dict.keys())[0]
        ingredients = recipe_dict[(meal_type, name)]

        # Create list to hold the ingredients for building Recipe object.
        ingredient_objects = []

        # Fill ingredient_objects list
        for ingredient in ingredients:
            # Generic quantity value
            quantity = 1

            # Get category
            category = categorise_ingredient(ingredient)

            # Add to list
            ingredient_objects.append(Ingredient(
                name=ingredient, quantity=quantity, category=category))

        return Recipe(name=name, ingredients=ingredient_objects, type=meal_type)


#### Food Ideas ####
"""
- Roast shrimp and veggie salad
- More Salads & healthy options
"""

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

### Recipes list: ###

# Tim's Meals

Bacon_Broccoli_Fryup = Recipe(
    name='Bacon Broccoli Fry-up',
    ingredients=[
        Ingredient(name='Bacon', quantity=1, category='Meat'),
        Ingredient(name='Broccoli', quantity=1, category='Frozen'),
        Ingredient(name='Olive Oil', quantity=1, category='Long-life'),
        Ingredient(name='Mushrooms', quantity=1, category='Veg'),
        Ingredient(name='Leeks', quantity=1, category='Veg'),
        Ingredient(name='Parmesan/Halloumi', quantity=1, category='Dairy')
        ],
    type='Tim')

Burritos = Recipe(
    name='Burritos',
    ingredients=[
        Ingredient(name='Mince/Chicken', quantity=1, category="Meat"),
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
        Ingredient(name='Yoghurt/Cream', quantity=1, category='Dairy')
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
        Ingredient(name='Mince/Pulled Chicken', quantity=1, category='Meat'),
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
        Ingredient(name='Meat Topping', quantity=1, category='Meat'),
        Ingredient(name='Mushrooms', quantity=1, category='Veg'),
        Ingredient(name='Peppers', quantity=1, category='Veg'),
        Ingredient(name='Tomato Puree', quantity=1, category='Long-life')
    ],
    type='Tim')

Steak = Recipe(
    name='Steak',
    ingredients=[
        Ingredient(name='Steak', quantity=1, category='Meat'),
        Ingredient(name='Broccoli/Asparagus', quantity=1, category='Veg'),
        Ingredient(name='Chips/Potatoes', quantity=1, category='Veg'),
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
        Ingredient(name='Chicken/Steak', quantity=1, category='Meat')
    ],
    type='Tim')

Carmelised_Onion_Sausages = Recipe(
    name='Carmelised Onion Sausages',
    ingredients=[
        Ingredient(name='Onions', quantity=1, category='Veg'),
        Ingredient(name='Peppers', quantity=1, category='Veg'),
        Ingredient(name='Garlic', quantity=1, category='Veg'),
        Ingredient(name='Green Beans', quantity=1, category='Frozen'),
        Ingredient(name='Parsely', quantity=1, category='Herbs/Spices'),
        Ingredient(name='Sausages', quantity=1, category='Meat'),
        Ingredient(name='Tomato Puree', quantity=1, category='Long-life'),
        Ingredient(name='Paprika', quantity=1, category='Herbs/Spices'),
        Ingredient(name='Rice', quantity=1, category='Long-life'),
        Ingredient(name='Chicken Stock', quantity=1, category='Long-life'),
        Ingredient(name='Cheddar', quantity=1, category='Dairy'),
        Ingredient(name='Chilli', quantity=1, category='Veg')
    ],
    type='Tim')


Spiced_Pork_Ragu = Recipe(
    name='Spiced Pork Ragu',
    ingredients=[
        Ingredient(name='Pasta', quantity=1, category='Long-life'),
        Ingredient(name='Spinach', quantity=1, category='Veg'),
        Ingredient(name='Garlic', quantity=1, category='Veg'),
        Ingredient(name='Chopped Tomatoes', quantity=1, category='Frozen'),
        Ingredient(name='Parsely', quantity=1, category='Herbs/Spices'),
        Ingredient(name='Sausages', quantity=1, category='Meat'),
        Ingredient(name='Tomato Puree', quantity=1, category='Long-life'),
        Ingredient(name='Cheddar', quantity=1, category='Dairy'),
        Ingredient(name='Chilli Flakes', quantity=1, category='Herbs/Spices')
    ],
    type='Tim')

Prawn_Chorizo_Rice = Recipe(
    name='Prawn Chorizo Rice',
    ingredients=[
        Ingredient(name='Plum Tomatoes', quantity=1, category='Veg'),
        Ingredient(name='Peppers', quantity=1, category='Veg'),
        Ingredient(name='Garlic', quantity=1, category='Veg'),
        Ingredient(name='Ciabatta', quantity=1, category='Bread'),
        Ingredient(name='Parsely', quantity=1, category='Herbs/Spices'),
        Ingredient(name='Chorizo', quantity=1, category='Meat'),
        Ingredient(name='Tomato Puree', quantity=1, category='Long-life'),
        Ingredient(name='Paprika', quantity=1, category='Herbs/Spices'),
        Ingredient(name='Rice', quantity=1, category='Long-life'),
        Ingredient(name='Prawns', quantity=1, category='Frozen'),
        Ingredient(name='Cheddar', quantity=1, category='Dairy')
    ],
    type='Tim')

Loaded_Wedges = Recipe(
    name='Mexican Loaded Wedges',
    ingredients=[
        Ingredient(name='Spring Onion', quantity=1, category='Veg'),
        Ingredient(name='Peppers', quantity=1, category='Veg'),
        Ingredient(name='Garlic', quantity=1, category='Veg'),
        Ingredient(name='Potatoes', quantity=1, category='Veg'),
        Ingredient(name='Lime', quantity=1, category='Veg'),
        Ingredient(name='Mince/Chicken', quantity=1, category='Meat'),
        Ingredient(name='Tomato Passata', quantity=1, category='Veg'),
        Ingredient(name='Paprika', quantity=1, category='Herbs/Spices'),
        Ingredient(name='Beef Stock/Chicken Stock',
                   quantity=1, category='Long-life'),
        Ingredient(name='Cheddar', quantity=1, category='Dairy'),
        Ingredient(name='Black Beans', quantity=1, category='Long-life'),
        Ingredient(name='Carrots', quantity=1, category='Veg')
    ],
    type='Tim')

# Freya's Meals

Sweet_and_Sour_Chicken = Recipe(
    name='Sweet and Sour Chicken',
    ingredients=[
        Ingredient(name='Garlic', quantity=1, category='Veg'),
        Ingredient(name='Rice Vinegar', quantity=1, category='Long-life'),
        Ingredient(name='Red Onions', quantity=1, category='Veg'),
        Ingredient(name='Cornflour', quantity=1, category='Long-life'),
        Ingredient(name='Spring Onion', quantity=1, category='Veg'),
        Ingredient(name='Vegetable Stock', quantity=1,
                   category='Herbs/Spices'),
        Ingredient(name='Rice', quantity=1, category='Long-life'),
        Ingredient(name='Chicken', quantity=1, category='Meat'),
        Ingredient(name='Ketjap Manis', quantity=1, category='Condiment'),
        Ingredient(name='Peppers', quantity=1, category='Veg')
    ],
    type='Freya')

Chicken_Chow_Mein = Recipe(
    name='Chicken Chow Mein',
    ingredients=[
        Ingredient(name='Oyster Sauce', quantity=1, category='Long-life'),
        Ingredient(name='Sesame Oil', quantity=1, category='Long-life'),
        Ingredient(name='Green Beans', quantity=1, category='Frozen'),
        Ingredient(name='Spring Onion', quantity=1, category='Veg'),
        Ingredient(name='Noodles', quantity=1, category='Long-life'),
        Ingredient(name='Chicken', quantity=1, category='Meat'),
        Ingredient(name='Ketjap Manis', quantity=1, category='Condiment'),
        Ingredient(name='Corn Starch', quantity=1, category='Long-life'),
        Ingredient(name='Chicken Stock', quantity=1, category='Long-life'),
        Ingredient(name='Sugar', quantity=1, category='Long-life'),
        Ingredient(name='Peppers', quantity=1, category='Veg')
    ],
    type='Freya')

Shepherds_Pie = Recipe(
    name='Shepherds Pie',
    ingredients=[
        Ingredient(name='Potatoes', quantity=1, category='Veg'),
        Ingredient(name='Lamb Mince', quantity=1, category='Meat'),
        Ingredient(name='Tomato Puree', quantity=1, category='Long-life'),
        Ingredient(name='Onions', quantity=1, category='Veg'),
        Ingredient(name='Carrots', quantity=1, category='Long-life'),
        Ingredient(name='Butter', quantity=1, category='Dairy'),
        Ingredient(name='Worcestershire Sauce',
                   quantity=1, category='Condiment'),
        Ingredient(name='Milk', quantity=1, category='Milk'),
        Ingredient(name='Beef Stock', quantity=1, category='Long-life'),
        Ingredient(name='Cheddar', quantity=1, category='Dairy')
    ],
    type='Freya')

Chicken_Fried_Rice = Recipe(
    name='Chicken Fried Rice',
    ingredients=[
        Ingredient(name='Onions', quantity=1, category='Veg'),
        Ingredient(name='Egg', quantity=1, category='Dairy'),
        Ingredient(name='Garlic', quantity=1, category='Veg'),
        Ingredient(name='Ginger', quantity=1, category='Veg'),
        Ingredient(name='Carrots', quantity=1, category='Veg'),
        Ingredient(name='Peas', quantity=1, category='Frozen'),
        Ingredient(name='Spring Onion', quantity=1, category='Veg'),
        Ingredient(name='Soy Sauce', quantity=1, category='Condiment'),
        Ingredient(name='Rice', quantity=1, category='Long-life'),
        Ingredient(name='Chicken Thighs', quantity=1, category='Meat'),
        Ingredient(name='Sesame Oil', quantity=1, category='Long-life'),
        Ingredient(name='Chinese 5 Spice', quantity=1, category='Herbs/Spices')
    ],
    type='Freya')

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
        Ingredient(name='Broccoli/Asparagus', quantity=1, category='Veg'),
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
        Ingredient(name='Rose Harissa Paste',
                   quantity=1, category='Herbs/Spices'),
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
        Ingredient(name='Mild Curry Powder',
                   quantity=1, category='Herbs/Spices'),
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
        Ingredient(name='Honey Mustard Dressing',
                   quantity=1, category='Condiment')
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


Lentil_Feta_Salad = Recipe(
    name='Lentil Feta Salad', 
    ingredients=[
        Ingredient(name='Green Lentils', quantity=1, category='Long-life'),
        Ingredient(name='Spring Onion', quantity=1, category='Veg'), 
        Ingredient(name='Feta', quantity=1, category='Dairy'),
        Ingredient(name='Parsely', quantity=1, category='Herbs/Spices'),
        Ingredient(name='Leaves', quantity=1, category='Veg'),
        Ingredient(name='Thyme', quantity=1, category='Herbs/Spices'),
        Ingredient(name='Oregano', quantity=1, category='Herbs/Spices'),
        Ingredient(name='Chili Flakes', quantity=1, category='Herbs/Spices'),
        Ingredient(name='Balsamic Vinegar', quantity=1, category='Condiment'),
        Ingredient(name='Olive Oil', quantity=1, category='Long-life')
        ],
    type='Healthy')

