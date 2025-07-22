# Code must be with SRP write
#======================
# class User:
#     def __init__(self, name, email):
#         self.name = name
#         self.email = email
#
#     def save(self):
#         print(f"{self.name} veritabanına kaydedildi.")
#
#     def send_welcome_email(self):
#         print(f"{self.email} adresine hoş geldin e-postası gönderildi.")


# With SRP injection code!
#=========================
# class User:
#     def __init__(self, name:str, email:str):
#         self.name = name
#         self.email = email
#
# class Save(User):
#     def save(self):
#         print(f"{self.name} veritabanına kaydedildi.")
#
#
# class Send_email(User):
#     def send_welcome_email(self):
#          print(f"{self.email} adresine hoş geldin e-postası gönderildi.")
#
#
# user = User("Ferdi", "tokyodrift@abv.bg")
# Save.save(user)
# Send_email.send_welcome_email(user)


class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class User_saver:
    @staticmethod
    def save(user: User):
        print(f"{user.name} veritabanına kaydedildi.") # self.name called with classname.objectname

class Email_sender:
    @staticmethod
    def send_welcome_email(user: User):
        print(f"{user.email} adresine hoş geldin e-postası gönderildi.")

user = User("Ayşe", "ayse@example.com")
User_saver.save(user)
Email_sender.send_welcome_email(user)