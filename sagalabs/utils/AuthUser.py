from sagalabs.utils.User import User

class AuthUser:

    def __init__(self, profile):
        self.profile = profile

    @property
    def id(self):
        return self.profile["user_id"]

    @property
    def email(self):
        return self.profile["email"]

    @property
    def user_type(self):
        return self.profile.get("UserType", User.DEFAULT_CLAIMS["UserType"])