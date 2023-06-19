class User:
    DEFAULT_CLAIMS = {'UserType': 'Admin'}

    def __init__(self, user_record):
        self.user_record = user_record

    @property
    def id(self):
        return self.user_record.uid

    @property
    def display_name(self):
        return self.user_record.display_name

    @property
    def email(self):
        return self.user_record.email

    @property
    def local_claims(self):
        custom_claims = self.user_record.custom_claims or {}
        claims = {}
        for claim, value in self.DEFAULT_CLAIMS.items():
            claims[claim] = custom_claims.get(claim, value)
        return claims