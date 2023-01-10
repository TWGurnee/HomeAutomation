import sqlite3 as db
from pathlib import Path

import Exercise.exercise as e
import Mealplan.recipes as r

  
class Database(object):
    """sqlite3 database class for mealplan and exercise manipulation"""

    DB_NAME = Path(r"database.db") #TODO Move to `YAML` config file to ensure secure.
    conn = db.connect(DB_NAME)
    cursor = conn.cursor()


    # Context manager functions # 
    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()

    # Initialisation methods #

    # Helper functions # 

    # Data manipulation methods #

