import sqlite3

from ..Exercise import exercise as e
from ..Mealplan import recipes as r



class Database(object):
    """sqlite3 database class that holds testers jobs"""
    DB_LOCATION = "/root/Documents/testerJobSearch/tester_db.sqlite"

    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cursor.close()
        if isinstance(exc_value, Exception):
            self.connection.rollback()
        else:
            self.connection.commit()
        self.connection.close()
