class Login:
    def __init__(self):
        self.db = []
    def add_user(self, username, password):
        self.db.append({'username': username, 'password': password})
    def login(self, username, password):
        for user in self.db:
            if user['username'] == username and user['password'] == password:
                return True
        return False