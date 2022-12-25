import recipes as r

# meal = {('type', 'name') : [ingredients]

meal = {('', ''):[]}

Test_Recipe = {('Tim', 'Steak'): ['Steak', 'Broccoli/Asparagus', 'Chips/Potatoes', 'Peppercorn Sauce']}

#print(r.Recipe.generate_recipe(meal))

types = {t.type for t in r.Recipe.All_Recipes}

print(types)