###########################################################
# classes.py                                              #
# All self-defined class definitions would be stored here #
###########################################################

class st1_cleared:
    def __init__(self):
        self.users = []
        self.version = "v1.0.1-alpha.1" # So that i'd know what attributes it (the class) has
    
    def add_waiting_user(self, id: str, email_id: str, password: str):
        self.users.append({
            'user_id': id,
            'email_id': email_id,
            'password': password
        })
    
    def delete_waiting_user_by_id(self, id: str): # Possible security issue. Password could have been asked, but as this only would occur on the server side. didnt really think of it much.
        for user in self.users:
            if user['user_id'] == id:
                self.users.remove(user)
                return True
            
        return False
    
    def search_record_by_id(self, id: str):
        for i in self.users:
            if i['user_id'] == id:
                return i
        
        return False

class Banned:
    def __init__(self):
        self.version = "v1.0.0=prealpha.1"
        self.banned = False