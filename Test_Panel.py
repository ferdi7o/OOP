from abc import ABC, abstractmethod

class MessageService(ABC):
    @abstractmethod
    def send(self, message):
        pass

class EmailService(MessageService):
    def send(self, message):
        print(f"E-posta gönderildi: {message}")

class SMSService(MessageService):
    def send(self, message):
        print(f"SMS gönderildi: {message}")

class Notification:
    def __init__(self, service: MessageService):
        self.service = service

    def notify(self, msg):
        self.service.send(msg)

email_notifier = Notification(EmailService())
email_notifier.notify("Toplantı saat 15:00'te.")

sms_notifier = Notification(SMSService())
sms_notifier.notify("Kodunuz: 123456")
