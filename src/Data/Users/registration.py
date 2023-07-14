import bcrypt


class PasswordDatabase: 

    def __init__(self):  
        self.data = dict() 
    
    def register(self, user, password):  # We want to send this to the users table, INSERT INTO users (email_address, password) VALUES (%s, %s)
        if user in self.data: # Needs a DB check.
          return False  
        pwd_hash = self.hash_password(password)  
        self.data[user] = pwd_hash #Replace with DB insert.
        return True 
    
    def login(self, user, password):  
        if user not in self.data: # Needs a DB check.
          return False  
        pwd_bytes = password.encode("utf-8")  
        return bcrypt.checkpw(pwd_bytes, self.data[user]) # replace the self.data[user] with password check. This info is hashed with the salt.
    
    def hash_password(self, password):  
        pwd_bytes = password.encode("utf-8")  
        salt = bcrypt.gensalt()  
        return bcrypt.hashpw(pwd_bytes, salt)
    
    # self.data should be replaced with the DB access. 
    # Doesn't appear that bcrypt requires the salt to be saved in the DB??

    # TODO add error checking messaging.