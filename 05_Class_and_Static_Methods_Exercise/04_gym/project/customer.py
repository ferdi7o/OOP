from project.id_mixin import IdMixin


class Customer(IdMixin):
    # ID = 1
    def __init__(self, name: str, address: str, email: str):
        self.name = name
        self.address = address
        self.email = email
        self.id = self.get_next_id()
        self.increment_id()

    # @classmethod
    # def get_next_id(cls):
    #     cls.ID += 1
    #     return cls.ID

    def __repr__(self):
        return (f"Customer <{self.id}> {self.name}; Address: {self.address}; "
                f"Email: {self.email}")
