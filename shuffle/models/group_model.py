class GroupModel:
    def __init__(self, members):
        self.members = members

    def get_members(self):
        return self.members

    def __str__(self):
        return str(len(self.members))

    def __len__(self):
        return len(self.members)

    def __repr__(self):
        return repr(self.members)