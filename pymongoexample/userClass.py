from flask_login import UserMixin

class User(UserMixin):
    id = None
    email = None
    password = None
    firstName = None
    lastName = None
    username = None
    date = None

    def getUserData(self,data):
        self.username = data['user']
        self.firstName = data['first name']
        self.lastName = data['last name']
        self.password = data['password']
        self.date = data['date']
