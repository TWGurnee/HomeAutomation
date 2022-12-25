import recipes as r

# meal = {('type', 'name') : [ingredients]
# Test_Recipe = {('Tim', 'Steak'): ['Steak', 'Broccoli/Asparagus', 'Chips/Potatoes', 'Peppercorn Sauce']}

meal = {('', ''):[]}

print(r.Recipe.generate_recipe(meal))