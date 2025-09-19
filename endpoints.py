from login import Login

class Endpoints:
    def __init__(self):
        self.login = Login()
    def add_user_endpoint(self, username, password):
        self.login.add_user(username, password)
        return 'User added successfully'
    def login_endpoint(self, username, password):
        if self.login.login(username, password):
            return 'Login successful'
        else:
            return 'Invalid username or password'