from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.app import App

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super(MainMenuScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', spacing=10, padding=50)

        start_button = Button(text='Oyuna Başla', size_hint=(1, 0.2))
        about_button = Button(text='Hakkımızda', size_hint=(1, 0.2))
        exit_button = Button(text='Çıkış', size_hint=(1, 0.2))

        start_button.bind(on_release=lambda x: setattr(self.manager, 'current', 'game'))
        about_button.bind(on_release=lambda x: setattr(self.manager, 'current', 'about'))
        exit_button.bind(on_release=lambda x: App.get_running_app().stop())

        layout.add_widget(start_button)
        layout.add_widget(about_button)
        layout.add_widget(exit_button)

        self.add_widget(layout)
