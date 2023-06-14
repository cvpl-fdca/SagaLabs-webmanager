class User:
    def __init__(self, name):
        self.name = name
        self.id = None
        self.status = "Active"
        self.exp = None
        self.connected = False
        self.connections = 0

    def __repr__(self) -> str:
        return f"<User: {self.name}>"


def from_obj(obj) -> User:
    u = User(obj['Identity'])
    u.status =  obj['AccountStatus']
    u.exp = obj['ExpirationDate']
    u.connections = obj['Connections']

    if obj['ConnectionStatus']:
        u.connected = True

    if 'id' in obj:
        u.id = obj['id']

    return u
