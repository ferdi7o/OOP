from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def __init__(self, height: int, width: int):
        self.height = height
        self.width = width

    def area(self):
        return self.height * self.width

class Square(Shape):
    def __init__(self, side: int):
        self.side = side

    def area(self):
        return self.side * self.side

def print_area(shape: Shape):
    print(f"Alan: {shape.area()}")

print_area(Rectangle(3, 4))  # Alan: 12
print_area(Square(5))        # Alan: 25
