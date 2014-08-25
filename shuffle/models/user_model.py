class UserModel:
    def __init__(self, email):
        self.email = email

    def get_email(self):
        return self.email

    def __str__(self):
        return self.email