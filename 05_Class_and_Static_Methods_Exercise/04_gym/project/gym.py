from project.customer import Customer
from project.equipment import Equipment
from project.exercise_plan import ExercisePlan
from project.id_mixin import IdMixin
from project.subscription import Subscription
from project.trainer import Trainer


class Gym(IdMixin):
    def __init__(self):
        self.id = self.get_next_id()
        self.increment_id()
        self.customers: list[Customer] = []
        self.subscriptions: list[Subscription] = []
        self.trainers: list[Trainer] = []
        self.equipment: list[Equipment] = []
        self.plans: list[ExercisePlan] = []

    def add_customer(self, customer: Customer):
        if customer not in self.customers:
            self.customers.append(customer)

    def add_trainer(self, trainer: Trainer):
        if trainer not in self.trainers:
            self.trainers.append(trainer)

    def add_equipment(self, equipment: Equipment):
        if equipment not in self.equipment:
            self.equipment.append(equipment)

    def add_plan(self, plan: ExercisePlan):
        if plan not in self.plans:
            self.plans.append(plan)

    def add_subscription(self, subscription: Subscription):
        if subscription not in self.subscriptions:
            self.subscriptions.append(subscription)

    def subscription_info(self, subscription_id: int):
        subs = next((s for s in self.subscriptions if s.id == subscription_id), None)
        cust = next((c for c in self.customers if c.id == subs.customer_id), None)
        trai = next((t for t in self.trainers if t.id == subs.trainer_id), None)
        plan = next((p for p in self.plans if p.id == subs.exercise_id), None)
        equi = next((e for e in self.equipment if e.id == plan.equipment_id), None)

        return "\n".join([subs.__repr__(),
                          cust.__repr__(),
                          trai.__repr__(),
                          equi.__repr__(),
                          plan.__repr__(),])

