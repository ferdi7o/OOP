from abc import ABC, abstractmethod


class Logger(ABC):
    @abstractmethod
    def log(self, user):
        pass

class ConsoleLogger(Logger):
    def log(self, user):
        print(f"Successfully logged {user} to the console")

class FileLogger(Logger):
    def log(self, user):
        print(f"Successfully logged {user} to the file")

class App:
    def __init__(self, logger: Logger):
        self.logger = logger

    def apply(self, usr):
        self.logger.log(usr)


user1 = App(ConsoleLogger())
user1.apply("Ferdi")

user2 = App(FileLogger())
user2.apply("Akif")