class Vehicle:
    def __init__(self, mileage: int, max_speed = 150):
        self.mileage = mileage
        self.max_speed = max_speed
        self.gadgets = []

    def speed_upper(self, speed_up):
        self.max_speed += speed_up
        return self.max_speed

car = Vehicle(20)
print(car.max_speed)
print(car.mileage)
print(car.gadgets)
car.gadgets.append('Hudly Wireless')
print(car.gadgets)
print(car.speed_upper(10))