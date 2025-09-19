from endpoints import Endpoints

class App:
    def __init__(self):
        self.endpoints = Endpoints()
    def run(self):
        print('1. Add user')
        print('2. Login')
        choice = input('Enter your choice: ')
        if choice == '1':
            username = input('Enter username: ')
            password = input('Enter password: ')
            print(self.endpoints.add_user_endpoint(username, password))
        elif choice == '2':
            username = input('Enter username: ')
            password = input('Enter password: ')
            print(self.endpoints.login_endpoint(username, password))