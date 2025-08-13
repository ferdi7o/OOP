from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class AboutScreen(Screen):
    def __init__(self, **kwargs):
        super(AboutScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)

        info_label = Label(
            text="Bu oyun OOP dersi için geliştirilmiştir.\nKüp oyununa hoş geldiniz!",
            halign='center', valign='middle'
        )

        back_button = Button(text='Ana Menüye Dön', size_hint=(1, 0.2))
        back_button.bind(on_release=lambda x: setattr(self.manager, 'current', 'main'))

        layout.add_widget(info_label)
        layout.add_widget(back_button)
        self.add_widget(layout)
