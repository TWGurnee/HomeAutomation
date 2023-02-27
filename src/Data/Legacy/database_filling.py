

    # ## Filling Fatabase Tables ###

    # @classmethod
    # def fill_ingredients(cls):
    #     for ingredient in Ingredient.All_Ingredients:
    #         name, quantity, category = astuple(ingredient)
    #         cls.cursor.execute("""
    #             INSERT INTO ingredients (ingredient_name,ingredient_shopping_category)
    #             VALUES (?, ?)""", (name, category,))
    #     cls.conn.commit()


    # @classmethod
    # def fill_recipes(cls):
    #     for recipe in Recipe.All_Recipes:
    #         name, ingredients, type = astuple(recipe)
    #         cls.cursor.execute("""
    #             INSERT INTO recipes (recipe_name, recipe_type)
    #             VALUES (?, ?)""", (name, type,))
    #     cls.conn.commit()


    # @classmethod
    # def fill_recipe_ingredients(cls):
    #     recipes_table = list(cls.cursor.execute("SELECT * FROM recipes"))
    #     ingredients_table = list(cls.cursor.execute("SELECT * FROM ingredients"))

    #     def get_ingredient_id_from_name(name):
    #         id = {i[1]: i[0] for i in ingredients_table}
    #         return id.get(name)

    #     for id, name, category in recipes_table:
    #         # get ingredients from recipe
    #         recipe = Recipe.get_recipe_from_name(name)
    #         recipe_id = id
    #         recipe_ingredient_ids = [get_ingredient_id_from_name(i.name) for i in recipe.ingredients] # type: ignore

    #         for ing_id in recipe_ingredient_ids:

    #             cls.cursor.execute("""
    #                 INSERT INTO recipe_ingredients (ingredient_quantity, recipe_id, ingredient_id)
    #                 VALUES (?, ?, ?)""",
    #                 (1, recipe_id, ing_id)
    #             )
    #     cls.conn.commit()

    # @classmethod
    # def fill_exercises(cls):
    #     for exercise in ALL_EXERCISES.exercises:
    #         name, type, muscle_group, weight, reps, time, secondary_type = exercise.to_tuple()
    #         cls.conn.execute("""
    #             INSERT INTO exercises (exercise_name,exercise_type,exercise_secondary_type,exercise_musclegroup,exercise_weight,exercise_reps,exercise_time)
    #             VALUES (?, ?, ?, ?, ?, ?, ?)""", (name, type, secondary_type, muscle_group, weight, reps, time,))
    #     cls.conn.commit()


# with PSQL.Database() as db:
#     db.cursor.execute("SELECT * FROM recipes") 
#     recipes_table = list(db.cursor.fetchall())

#     db.cursor.execute("SELECT * FROM ingredients")
#     ingredients_table = list(db.cursor.fetchall())

#     def get_ingredient_id_from_name(name):
#         id = {i[1]: i[0] for i in ingredients_table}
#         return id.get(name)
    

#     for id, name in recipes_table:
#         # get ingredients from recipe
#         recipe = Database.get_recipe_from_name(name)
#         recipe_id = id
#         recipe_ingredient_ids = [PSQL.Database.get_item_id("ingredients", i.name) for i in recipe.ingredients] # type: ignore
#         for ing_id, ing in zip(recipe_ingredient_ids, recipe.ingredients):
            
#             quantity = input(f"insert quantity of {ing.name} used in {recipe.name}: ")

#             unit = input(f'what unit of measurement is used for {ing.name}: ')
#             if unit == "" or " ": quantity = None

#             db.cursor.execute("""
#                 INSERT INTO recipe_ingredients (ingredient_quantity, ingredient_unit, recipe_id, ingredient_id)
#                 VALUES (%s, %s, %s, %s)""",
#                 (quantity, unit, recipe_id, ing_id)
#             )
