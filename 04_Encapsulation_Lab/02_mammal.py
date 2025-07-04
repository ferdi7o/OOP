class Mammal:
    __kingdom = "animals"

    def __init__(self, name: str, type: type, sound):
        self.name = name
        self.type = type
        self.sound = sound

    def make_sound(self):
        return f"{self.name} makes {self.sound}"

mammal = Mammal("Dog", "Domestic", "Bark")
print(mammal.make_sound())
print(mammal.get_kingdom())
print(mammal.info())

