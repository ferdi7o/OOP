class Example:
    text = "Hello"

    def __init__(self, name):
        self.name = name

ex1 = Example("W124")
ex2 = Example("W--")
print(ex1.text)
print(ex1.name)
ex1.name = "ferdi"
print(ex1.name)
print(ex2.text)
print(ex2.name)
Example.text = "WORLD"
print(ex2.text)
print(ex1.text)
ex1.text = "Tokyo drift"
print(ex1.text)
print(ex2.text)