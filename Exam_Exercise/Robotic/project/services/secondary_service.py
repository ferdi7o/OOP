from project.services.base_service import BaseService


class SecondaryService(BaseService):
    CAPACITY = 15

    def __init__(self, name: str):
        super().__init__(name, self.CAPACITY)

    def details(self):
        result = (f"{self.name} Secondary Service:\n"
                  f"Robots: {' '.join(n.name for n in self.robots) if self.robots else 'none'}")
        return result