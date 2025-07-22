from abc import ABC, abstractmethod


class Payment_strategy(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class Cash_payment(Payment_strategy):
    def pay(self, amount):
        return amount - (amount * 0.01) #discount per cash payment

class Card_payment(Payment_strategy):
    def pay(self, amount):
        return amount

class Payment_processing:
    def __init__(self, amount: Payment_strategy):
        self.amount = amount

    def get_price(self, price):
        return self.amount.pay(price)


cash_price = Cash_payment()
calc = Payment_processing(cash_price)
print(calc.get_price(100))

card_price = Card_payment()
calc = Payment_processing(card_price)
print(calc.get_price(100))