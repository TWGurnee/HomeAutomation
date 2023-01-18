DROP TABLE IF EXISTS ingredients;
DROP TABLE IF EXISTS recipes;
DROP TABLE IF EXISTS recipe_ingredients;
DROP TABLE IF EXISTS exercises;


CREATE TABLE IF NOT EXISTS ingredients (
    ingredient_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ingredient_name TEXT NOT NULL,
    ingredient_shopping_category TEXT
);



CREATE TABLE IF NOT EXISTS recipes (
    recipe_id INTEGER,
    ingredient_id
    recipe_name TEXT NOT NULL,
    recipe_type TEXT NOT NULL,
);



CREATE TABLE IF NOT EXISTS recipe_ingredients (
    id INTERGER PRIMARY KEY AUTOINCREMENT,
    recipe_id INTEGER,
    ingredient_id INTEGER,
    FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
    FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id),
    ingredient_quantity INTEGER,
);



CREATE TABLE IF NOT EXISTS exercises (
    exercise_id INTEGER PRIMARY KEY AUTOINCREMENT,
    exercise_name TEXT NOT NULL,
    exercise_type TEXT NOT NULL,
    exercise_secondary_type TEXT
    exercise_musclegroup TEXT,
    exercise_weight FLOAT,
    exercise_weight_increment FLOAT,
    exercise_reps INTEGER,
    exercise_time INTEGER
);